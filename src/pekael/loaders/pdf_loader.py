"""PDF loader: native text per page, OCR fallback only for pages without enough text."""

from pathlib import Path

from langchain_core.documents import Document

from pekael.loaders.base import BaseLoader
from pekael.services.ocr_service import OcrService


class PDFLoader(BaseLoader):
    def __init__(self, ocr_service: OcrService | None = None, min_text_chars: int = 40) -> None:
        if min_text_chars < 0:
            raise ValueError("min_text_chars must be >= 0")
        self.ocr_service = ocr_service
        self.min_text_chars = min_text_chars

    def load(self, source_path: str | Path) -> list[Document]:
        raise NotImplementedError("PDFLoader.load is implemented in Sprint 1")
