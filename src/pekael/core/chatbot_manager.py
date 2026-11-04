"""Orchestrator of ingestion and question answering (class diagram: ChatbotManager).

There is deliberately no conversation memory: every question is answered independently.
"""

import logging
import time
from collections.abc import Callable
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

    def initialize_knowledge_base(self, source_path: str | Path) -> IngestionReport:
        """Load, split and index one approved PDF. A failed build keeps the previous index (FR-07)."""
        pages = self.loader.load(source_path)
        chunks = self.splitter.split(pages)
        indexing = self.vector_store.ingest_document(chunks)
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
        )

    def generate_response(self, message: str, on_step: Callable[[str], None] | None = None) -> ChatbotResponse:
        """Answer one question on its own; errors become a safe status response, never an answer.

        ``on_step`` receives the name of each step as it starts, so the UI can show progress.
        """
        started = time.perf_counter()
        config = {"callbacks": [_StepReporter(self.chain.step_names, on_step)]} if on_step else None
        try:
            response = self.chain.invoke(ChainState(question=message), config=config).response
        except Exception:  # a step failed in a way it did not handle itself
            logger.exception("Unexpected error while answering")
            response = None
        if response is None:
            response = ChatbotResponse(messages.UNEXPECTED_ERROR, ResponseStatus.ERROR)
        logger.info(
            "Answered with status=%s sources=%d nearest=%s in %.2f s",
            response.status.value,
            len(response.sources),
            f"{min(response.distances):.3f}" if response.distances else "-",
            time.perf_counter() - started,
        )
        return response
