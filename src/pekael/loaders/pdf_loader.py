"""PDF loader: native text per page, OCR fallback only for pages without enough text."""

import hashlib
from dataclasses import dataclass
from pathlib import Path

import pymupdf
from langchain_core.documents import Document
from PIL import Image

from pekael.loaders.base import BaseLoader
from pekael.loaders.text_cleaning import clean_page_text
from pekael.services.ocr_service import OcrResult, OcrService

NATIVE_TEXT = "native_text"
TESSERACT_OCR = "tesseract_ocr"


class DocumentLoadError(ValueError):
    """The source file is missing, not a PDF, encrypted, empty, or needs OCR that is not configured."""


@dataclass(frozen=True)
class PageExtraction:
    page: int  # 1-based physical PDF page
    raw_text: str  # before clean-up
    extraction_method: str
    ocr: OcrResult | None = None
    corrected: bool = False  # text comes from a manually verified correction file


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


class PDFLoader(BaseLoader):
    def __init__(
        self,
        ocr_service: OcrService | None = None,
        min_text_chars: int = 40,
        ocr_dpi: int = 200,
        corrections_dir: str | Path | None = None,
    ) -> None:
        if min_text_chars < 0:
            raise ValueError("min_text_chars must be >= 0")
        if ocr_dpi <= 0:
            raise ValueError("ocr_dpi must be > 0")
        self.ocr_service = ocr_service
        self.min_text_chars = min_text_chars
        self.ocr_dpi = ocr_dpi
        self.corrections_dir = Path(corrections_dir) if corrections_dir else None

    def load(self, source_path: str | Path) -> list[Document]:
        """Return one Document per PDF page, in page order."""
        path = Path(source_path)
        pdf = self.open_pdf(path)
        source_hash = file_sha256(path)
        try:
            return [
                self.to_document(self.extract_page(page, source_hash), path.name, source_hash, pdf.page_count)
                for page in pdf
            ]
        finally:
            pdf.close()

    @staticmethod
    def open_pdf(path: Path) -> pymupdf.Document:
        if not path.is_file():
            raise DocumentLoadError(f"File not found: {path}")
        try:
            pdf = pymupdf.open(path, filetype="pdf")
        except Exception as exc:  # PyMuPDF raises several error types for corrupt files
            raise DocumentLoadError(f"Not a readable PDF: {path.name}") from exc
        if pdf.needs_pass:
            pdf.close()
            raise DocumentLoadError(f"PDF is password protected: {path.name}")
        if pdf.page_count == 0:
            pdf.close()
            raise DocumentLoadError(f"PDF has no pages: {path.name}")
        return pdf

    def correction_path(self, source_hash: str, page_number: int) -> Path | None:
        """Manually verified text for one page, stored per source version (OD-17)."""
        if self.corrections_dir is None:
            return None
        path = self.corrections_dir / source_hash[:12] / f"page_{page_number:03d}.txt"
        return path if path.is_file() else None

    def extract_page(self, page: pymupdf.Page, source_hash: str | None = None) -> PageExtraction:
        """Use a correction file if one exists for this source version, else native text, else OCR."""
        number = page.number + 1
        native = page.get_text()
        method = NATIVE_TEXT if len(native.strip()) >= self.min_text_chars else TESSERACT_OCR
        correction = self.correction_path(source_hash, number) if source_hash else None
        if correction is not None:
            return PageExtraction(number, correction.read_text(encoding="utf-8"), method, corrected=True)
        if method == NATIVE_TEXT:
            return PageExtraction(number, native, NATIVE_TEXT)
        if self.ocr_service is None:
            raise DocumentLoadError(f"Page {number} has no text layer and OCR is not configured")
        result = self.ocr_service.image_to_text(self.render(page))
        return PageExtraction(number, result.text, TESSERACT_OCR, result)

    @staticmethod
    def to_document(extraction: PageExtraction, source_file: str, source_hash: str, total_pages: int) -> Document:
        metadata = {
            "source_file": source_file,
            "source_hash": source_hash,
            "page": extraction.page,
            "total_pages": total_pages,
            "extraction_method": extraction.extraction_method,
            "manually_corrected": extraction.corrected,
        }
        if extraction.ocr is not None:
            metadata["ocr_mean_confidence"] = extraction.ocr.mean_confidence
            metadata["ocr_low_confidence_words"] = extraction.ocr.low_confidence_words
        return Document(page_content=clean_page_text(extraction.raw_text), metadata=metadata)

    def render(self, page: pymupdf.Page) -> Image.Image:
        pixmap = page.get_pixmap(dpi=self.ocr_dpi, colorspace=pymupdf.csGRAY)
        return Image.frombytes("L", (pixmap.width, pixmap.height), pixmap.samples)
