"""Orchestrator of ingestion and question answering (class diagram: ChatbotManager).

There is deliberately no conversation memory: every question is answered independently.
Answers are cached per (normalised question, knowledge base build), which is not memory:
no earlier question is ever sent with a new one (FR-10). The cache only avoids asking
Gemini the same question twice (free-tier quota and waiting time, D-41).
"""

import logging
import re
import threading
import time
from collections import OrderedDict
from collections.abc import Callable, Sequence
from pathlib import Path

from langchain_core.callbacks import BaseCallbackHandler

from pekael.core import messages
from pekael.core.chain import Chain
from pekael.core.rag_steps import RagSteps
from pekael.core.schemas import ChainState, ChatbotResponse, IngestionReport, ResponseStatus
from pekael.loaders.base import BaseLoader
from pekael.loaders.pdf_loader import TESSERACT_OCR
from pekael.models.gemini_model import GeminiModel
from pekael.splitters.base import BaseSplitter
from pekael.vectorstores.base import BaseVectorStore

logger = logging.getLogger(__name__)

CACHEABLE = (ResponseStatus.ANSWERED, ResponseStatus.OUT_OF_SCOPE)  # never cache errors or invalid input
BUILD_STAGES = ("load", "split", "index")


def normalise_question(message: str) -> str:
    """'  Berapa SKS  minimal?? ' -> 'berapa sks minimal'."""
    return re.sub(r"\s+", " ", message.strip().lower()).rstrip(" ?!.,")


class _StepReporter(BaseCallbackHandler):
    """Report each Chain step that actually runs (skipped steps are not reported)."""

    def __init__(self, step_names: list[str], on_step: Callable[[str], None]) -> None:
        self.step_names = set(step_names)
        self.on_step = on_step

    def on_chain_start(self, serialized, inputs, **kwargs) -> None:
        name = kwargs.get("name")
        if name in self.step_names and getattr(inputs, "response", None) is None:
            self.on_step(name)


class ChatbotManager:
    def __init__(
        self,
        system_prompt: str,
        loader: BaseLoader,
        splitter: BaseSplitter,
        vector_store: BaseVectorStore,
        llm: GeminiModel,
        chain: Chain | None = None,
        retrieval_k: int = 4,
        max_distance: float | None = None,
        question_max_chars: int = 500,
        cache_size: int = 256,
    ) -> None:
        self.system_prompt = system_prompt
        self.loader = loader
        self.splitter = splitter
        self.vector_store = vector_store
        self.llm = llm
        self.chain = chain or Chain()
        if not self.chain.step_names:
            steps = RagSteps(vector_store, llm, system_prompt, retrieval_k, max_distance, question_max_chars)
            steps.build_chain(self.chain)
        self.cache_size = cache_size
        self._cache: OrderedDict[tuple[str, str], ChatbotResponse] = OrderedDict()
        self._cache_lock = threading.Lock()

    # ---------- knowledge base ----------

    def initialize_knowledge_base(
        self,
        source_path: str | Path,
        pages: list[int] | None = None,
        on_progress: Callable[[str, int, int], None] | None = None,
        extra_paths: Sequence[str | Path] = (),
    ) -> IngestionReport:
        """Load, split and index the approved handbook pages plus any additional documents.

        A failed build keeps the previous index (FR-07). ``pages`` overrides the configured page
        selection of the handbook, ``extra_paths`` are further approved PDFs used in full (D-53).
        Every document is split on its own, so chunks never mix documents.
        ``on_progress(stage, done, total)`` reports the stages in BUILD_STAGES, with page counts while loading.
        """

        def report(stage: str, done: int = 0, total: int = 0) -> None:
            if on_progress:
                on_progress(stage, done, total)

        def on_page(done: int, total: int) -> None:
            report("load", done, total)

        report("load")
        loaded = [self.loader.load(source_path, pages=pages, on_page=on_page)]
        loaded += [self.loader.load(extra, on_page=on_page, all_pages=True) for extra in extra_paths]
        report("split")
        chunks = [chunk for documents in loaded for chunk in self.splitter.split(documents)]
        report("index", 0, len(chunks))
        build_info = getattr(self.vector_store, "build_info", None)
        if isinstance(build_info, dict):  # recorded in the manifest, so the admin can rebuild from the same files
            build_info["source_path"] = str(source_path)
            build_info["extra_paths"] = [str(p) for p in extra_paths]
            if pages is not None:
                build_info["knowledge_base_pages"] = ",".join(str(p) for p in sorted(set(pages)))
        indexing = self.vector_store.ingest_document(chunks)
        self.clear_cache()
        pages = [page for documents in loaded for page in documents]
        ocr_pages = [d for d in pages if d.metadata.get("extraction_method") == TESSERACT_OCR]
        unchecked = [d.metadata["page"] for d in ocr_pages if not d.metadata.get("manually_corrected")]
        warnings = (f"OCR pages without a correction file, confirm they were checked: {unchecked}",) if unchecked else ()
        return IngestionReport(
            source_file=pages[0].metadata["source_file"],
            source_hash=pages[0].metadata["source_hash"],
            page_count=len(pages),
            native_pages=len(pages) - len(ocr_pages),
            ocr_pages=len(ocr_pages),
            chunk_count=len(chunks),
            indexing=indexing,
            warnings=warnings,
            extra_sources=tuple(documents[0].metadata["source_file"] for documents in loaded[1:] if documents),
        )

    # ---------- start-up ----------

    def warm_up(self) -> float:
        """Load the index and open the embedding and Gemini connections before the first question.

        The first call of a fresh process is noticeably slower (about 3 s more for Gemini); doing it
        here, while the intro shows, keeps that wait away from students. Costs one embedding and one
        tiny Gemini request per server start. Failures are logged, never raised.
        """
        started = time.perf_counter()
        try:
            if hasattr(self.vector_store, "load") and not getattr(self.vector_store, "is_ready", False):
                self.vector_store.load()
            embeddings = getattr(self.vector_store, "embeddings", None)
            if embeddings is not None:
                embeddings.embed_query("PKL")
            self.llm.generate_response("Balas dengan satu kata: siap")
        except Exception as exc:  # warm-up is best effort; the real question reports errors properly
            logger.warning("Warm-up incomplete: %s", type(exc).__name__)
        seconds = time.perf_counter() - started
        logger.info("Warm-up finished in %.2f s", seconds)
        return seconds

    # ---------- answer cache ----------

    def _cache_key(self, message: str) -> tuple[str, str] | None:
        question = normalise_question(message)
        if not question:
            return None
        build_id = (getattr(self.vector_store, "manifest", None) or {}).get("build_id", "")
        return question, build_id

    def cached_answers(self) -> int:
        return len(self._cache)

    def clear_cache(self) -> None:
        with self._cache_lock:
            self._cache.clear()

    # ---------- answering ----------

    def generate_response(self, message: str, on_step: Callable[[str], None] | None = None) -> ChatbotResponse:
        """Answer one question on its own; errors become a safe status response, never an answer.

        ``on_step`` receives the name of each step as it starts, so the UI can show progress.
        A question asked before (same wording, same knowledge base build) is answered from the cache.
        """
        started = time.perf_counter()
        key = self._cache_key(message)
        with self._cache_lock:
            cached = self._cache.get(key) if key and self.cache_size else None
            if cached is not None:
                self._cache.move_to_end(key)
        if cached is not None:
            logger.info("Answered from cache with status=%s in %.2f s", cached.status.value, time.perf_counter() - started)
            return cached
        config = {"callbacks": [_StepReporter(self.chain.step_names, on_step)]} if on_step else None
        try:
            response = self.chain.invoke(ChainState(question=message), config=config).response
        except Exception:  # a step failed in a way it did not handle itself
            logger.exception("Unexpected error while answering")
            response = None
        if response is None:
            response = ChatbotResponse(messages.UNEXPECTED_ERROR, ResponseStatus.ERROR)
        key = self._cache_key(message)  # the build may have changed while answering
        if key and self.cache_size and response.status in CACHEABLE:
            with self._cache_lock:
                self._cache[key] = response
                while len(self._cache) > self.cache_size:
                    self._cache.popitem(last=False)
        logger.info(
            "Answered with status=%s sources=%d nearest=%s in %.2f s",
            response.status.value,
            len(response.sources),
            f"{min(response.distances):.3f}" if response.distances else "-",
            time.perf_counter() - started,
        )
        return response
