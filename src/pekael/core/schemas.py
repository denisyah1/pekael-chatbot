"""Data objects passed between pipeline components."""

from dataclasses import dataclass, field
from enum import Enum

from langchain_core.documents import Document


class ResponseStatus(str, Enum):
    ANSWERED = "answered"
    OUT_OF_SCOPE = "out_of_scope"
    INVALID_INPUT = "invalid_input"
    UNAVAILABLE = "unavailable"
    ERROR = "error"


def document_name(source_file: str) -> str:
    """'Pedoman-PKL-2025.pdf' -> 'Pedoman PKL 2025' (shown in prompts and citations)."""
    stem = source_file.replace("\\", "/").rsplit("/", 1)[-1]
    stem = stem[: -len(".pdf")] if stem.lower().endswith(".pdf") else stem
    return stem.replace("-", " ").replace("_", " ")


@dataclass(frozen=True)
class SourceReference:
    """A citation built from the metadata of a retrieved chunk, never from LLM output."""

    source_file: str
    page: int
    chunk_id: str
    section: str | None = None
    snippet: str | None = None


@dataclass(frozen=True)
class RetrievedDocument:
    document: Document
    distance: float  # FAISS L2 distance: smaller means closer; not a probability


@dataclass(frozen=True)
class ChatbotResponse:
    answer: str
    status: ResponseStatus
    sources: tuple[SourceReference, ...] = ()
    # Distances of the retrieved chunks, for logs and threshold calibration, not shown to students
    distances: tuple[float, ...] = ()


@dataclass(frozen=True)
class IndexingReport:
    build_id: str
    chunk_count: int
    embedding_model: str
    dimension: int
    index_path: str


@dataclass(frozen=True)
class IngestionReport:
    source_file: str
    source_hash: str
    page_count: int
    native_pages: int
    ocr_pages: int
    chunk_count: int
    indexing: IndexingReport | None = None
    warnings: tuple[str, ...] = ()
    extra_sources: tuple[str, ...] = ()  # file names of the additional documents (D-53)


@dataclass
class ChainState:
    """Mutable state carried through the Chain steps for one question.

    Once ``response`` is set (e.g. by the relevancy gate), remaining steps are skipped.
    """

    question: str
    retrieved: list[RetrievedDocument] = field(default_factory=list)
    distances: tuple[float, ...] = ()  # of every retrieved chunk, before the relevancy gate
    context: str = ""
    prompt: str = ""
    answer: str = ""
    response: ChatbotResponse | None = None
