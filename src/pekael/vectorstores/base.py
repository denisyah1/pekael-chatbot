from abc import ABC, abstractmethod

from langchain_core.documents import Document

from pekael.core.schemas import IndexingReport, RetrievedDocument


class BaseVectorStore(ABC):
    @abstractmethod
    def ingest_document(self, documents: list[Document]) -> IndexingReport:
        """Embed and index chunks."""

    @abstractmethod
    def get_relevant_document(self, query: str, k: int | None = None) -> list[RetrievedDocument]:
        """Return the k nearest chunks with their metadata and distance score."""
