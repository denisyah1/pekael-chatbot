"""Wrapper around LangChain's RecursiveCharacterTextSplitter."""

from langchain_core.documents import Document

from pekael.splitters.base import BaseSplitter


class RecursiveCharacterSplitter(BaseSplitter):
    def __init__(self, chunk_size: int, chunk_overlap: int) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be > 0")
        if not 0 <= chunk_overlap < chunk_size:
            raise ValueError("chunk_overlap must be >= 0 and smaller than chunk_size")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, documents: list[Document]) -> list[Document]:
        raise NotImplementedError("RecursiveCharacterSplitter.split is implemented in Sprint 2")
