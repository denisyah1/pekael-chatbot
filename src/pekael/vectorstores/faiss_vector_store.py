"""FAISS IndexFlatL2 vector store with versioned, persistent indexes."""

from pathlib import Path

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from pekael.core.schemas import IndexingReport, RetrievedDocument
from pekael.vectorstores.base import BaseVectorStore


class FaissVectorStore(BaseVectorStore):
    def __init__(self, index_path: str | Path, embeddings: Embeddings, default_k: int = 4) -> None:
        if default_k <= 0:
            raise ValueError("default_k must be > 0")
        self.index_path = Path(index_path)
        self.embeddings = embeddings
        self.default_k = default_k

    def ingest_document(self, documents: list[Document]) -> IndexingReport:
        raise NotImplementedError("FaissVectorStore.ingest_document is implemented in Sprint 3")

    def get_relevant_document(self, query: str, k: int | None = None) -> list[RetrievedDocument]:
        raise NotImplementedError("FaissVectorStore.get_relevant_document is implemented in Sprint 3")
