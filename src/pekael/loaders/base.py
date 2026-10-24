from abc import ABC, abstractmethod
from pathlib import Path

from langchain_core.documents import Document


class BaseLoader(ABC):
    @abstractmethod
    def load(self, source_path: str | Path) -> list[Document]:
        """Load a source into one Document per page, with source/page metadata."""
