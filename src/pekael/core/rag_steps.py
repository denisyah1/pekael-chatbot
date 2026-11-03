"""The question-answering steps of the Chain (spec §4.3, §12 Sprint 3).

validate_input -> retrieve -> relevancy_gate -> build_prompt -> generate -> validate_citations

Each step reads and updates one ChainState. A step that cannot continue (empty question,
missing index, irrelevant context, provider failure) sets ``state.response`` and the
remaining steps are skipped, so Gemini is not called when it is not needed.
"""

import logging
import re

from pekael.core import messages
from pekael.core.chain import Chain
from pekael.core.prompts import FALLBACK_MESSAGE, SYSTEM_PROMPT, build_user_prompt, format_context, parse_answer
from pekael.core.schemas import ChainState, ChatbotResponse, ResponseStatus, RetrievedDocument, SourceReference
from pekael.models.gemini_model import AUTH, QUOTA, UNAVAILABLE, GeminiModel, LLMError, classify_error
from pekael.vectorstores.base import BaseVectorStore, IndexNotReadyError

logger = logging.getLogger(__name__)

SNIPPET_CHARS = 200

_PROVIDER_MESSAGES = {
    QUOTA: messages.QUOTA_EXHAUSTED,
    UNAVAILABLE: messages.SERVICE_UNAVAILABLE,
    AUTH: messages.SERVICE_MISCONFIGURED,
}


def _provider_kind(exc: BaseException) -> str:
    """Classify an error by itself or by its cause (EmbeddingError wraps the provider error)."""
    kinds = [classify_error(e) for e in (exc, exc.__cause__) if e is not None]
    return next((k for k in kinds if k in _PROVIDER_MESSAGES), kinds[0])


def _snippet(text: str) -> str:
    flat = re.sub(r"\s+", " ", text).strip()
    return flat if len(flat) <= SNIPPET_CHARS else flat[:SNIPPET_CHARS].rsplit(" ", 1)[0] + " …"


def source_reference(item: RetrievedDocument) -> SourceReference:
    meta = item.document.metadata
    return SourceReference(
        source_file=meta["source_file"],
        page=int(meta["page"]),
        chunk_id=meta["chunk_id"],
        section=meta.get("section") or None,
        snippet=_snippet(item.document.page_content),
    )


class RagSteps:
    def __init__(
        self,
        vector_store: BaseVectorStore,
        llm: GeminiModel,
        system_prompt: str = SYSTEM_PROMPT,
        retrieval_k: int = 4,
        max_distance: float | None = None,
        question_max_chars: int = 500,
    ) -> None:
        self.vector_store = vector_store
        self.llm = llm
        self.system_prompt = system_prompt
        self.retrieval_k = retrieval_k
        self.max_distance = max_distance  # squared L2 (D-29); None = gate disabled until calibrated
        self.question_max_chars = question_max_chars

    def build_chain(self, chain: Chain | None = None) -> Chain:
        chain = chain or Chain()
        for step in (
            self.validate_input,
            self.retrieve,
            self.relevancy_gate,
            self.build_prompt,
            self.generate,
            self.validate_citations,
        ):
            chain.add(step, name=step.__name__)
        return chain

    def validate_input(self, state: ChainState) -> ChainState:
        state.question = state.question.strip()
        if not state.question:
            state.response = ChatbotResponse(messages.EMPTY_QUESTION, ResponseStatus.INVALID_INPUT)
        elif len(state.question) > self.question_max_chars:
            text = messages.QUESTION_TOO_LONG.format(limit=self.question_max_chars)
            state.response = ChatbotResponse(text, ResponseStatus.INVALID_INPUT)
        return state

    def retrieve(self, state: ChainState) -> ChainState:
        try:
            state.retrieved = self.vector_store.get_relevant_document(state.question, k=self.retrieval_k)
            state.distances = tuple(item.distance for item in state.retrieved)
        except IndexNotReadyError as exc:
            logger.warning("Knowledge base not ready: %s", exc)
            state.response = ChatbotResponse(messages.INDEX_NOT_READY, ResponseStatus.UNAVAILABLE)
            return state
        except Exception as exc:  # embedding (quota, key, network) or FAISS failure
            kind = _provider_kind(exc)
            logger.error("Retrieval failed (%s): %s", kind, type(exc).__name__)
            if kind in _PROVIDER_MESSAGES:
                state.response = ChatbotResponse(_PROVIDER_MESSAGES[kind], ResponseStatus.UNAVAILABLE)
            else:
                state.response = ChatbotResponse(messages.RETRIEVAL_FAILED, ResponseStatus.ERROR)
            return state
        if not state.retrieved:
            state.response = ChatbotResponse(FALLBACK_MESSAGE, ResponseStatus.OUT_OF_SCOPE)
        return state

    def relevancy_gate(self, state: ChainState) -> ChainState:
        """Keep only chunks within the calibrated distance; reject the question if none remain."""
        if self.max_distance is not None:
            state.retrieved = [item for item in state.retrieved if item.distance <= self.max_distance]
        if not state.retrieved:
            logger.info("Relevancy gate rejected question, nearest distance %.3f", min(state.distances))
            state.response = ChatbotResponse(FALLBACK_MESSAGE, ResponseStatus.OUT_OF_SCOPE, distances=state.distances)
        return state

    def build_prompt(self, state: ChainState) -> ChainState:
        state.context = format_context(state.retrieved)
        state.prompt = build_user_prompt(state.question, state.retrieved)
        return state

    def generate(self, state: ChainState) -> ChainState:
        try:
            state.answer = self.llm.generate_response(state.prompt, system_prompt=self.system_prompt)
        except LLMError as exc:
            logger.error("Generation failed (%s)", exc.kind)
            if exc.kind in _PROVIDER_MESSAGES:
                state.response = ChatbotResponse(_PROVIDER_MESSAGES[exc.kind], ResponseStatus.UNAVAILABLE)
            else:  # empty answer or an unclassified provider error
                state.response = ChatbotResponse(messages.GENERATION_FAILED, ResponseStatus.ERROR)
        return state

    def validate_citations(self, state: ChainState) -> ChainState:
        """Turn the model output into a response whose sources come only from retrieved chunks."""
        parsed = parse_answer(state.answer, len(state.retrieved))
        if parsed.not_found:
            state.response = ChatbotResponse(FALLBACK_MESSAGE, ResponseStatus.OUT_OF_SCOPE, distances=state.distances)
            return state
        if parsed.context_numbers is None:
            logger.warning("Answer has no valid SUMBER line, citing every context chunk")
            cited = state.retrieved
        else:
            cited = [state.retrieved[n - 1] for n in parsed.context_numbers]
        sources = tuple(source_reference(item) for item in cited)
        state.response = ChatbotResponse(parsed.answer, ResponseStatus.ANSWERED, sources, state.distances)
        return state
