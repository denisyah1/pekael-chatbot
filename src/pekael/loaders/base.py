from abc import ABC, abstractmethod
from collections.abc import Callable
from pathlib import Path

from langchain_core.documents import Document


class BaseLoader(ABC):
    @abstractmethod
    def load(
        self,
        source_path: str | Path,
        *,
        pages: list[int] | None = None,
        on_page: Callable[[int, int], None] | None = None,
    ) -> list[Document]:
        """Load a source into one Document per page, with source/page metadata.

        ``pages`` overrides the configured page selection, ``on_page(done, total)`` reports progress.
        """
