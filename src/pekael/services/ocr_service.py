"""Tesseract OCR, used only during ingestion for pages without a usable text layer."""

from PIL.Image import Image


class OcrService:
    def __init__(self, tesseract_cmd: str | None = None, lang: str = "ind+eng") -> None:
        self.tesseract_cmd = tesseract_cmd
        self.lang = lang

    def image_to_text(self, image: Image) -> str:
        raise NotImplementedError("OcrService.image_to_text is implemented in Sprint 1")
