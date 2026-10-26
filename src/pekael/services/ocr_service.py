"""Tesseract OCR, used only during ingestion for pages without a usable text layer."""

from dataclasses import dataclass

import pytesseract
from PIL.Image import Image

# Words below this Tesseract confidence (0-100) are counted as uncertain for manual review.
LOW_CONFIDENCE_THRESHOLD = 60


class OcrUnavailableError(RuntimeError):
    """Tesseract is missing, misconfigured, or lacks a required language."""


@dataclass(frozen=True)
class OcrResult:
    text: str
    mean_confidence: float | None  # None when no words were recognised
    word_count: int
    low_confidence_words: int


class OcrService:
    def __init__(self, tesseract_cmd: str | None = None, lang: str = "ind+eng") -> None:
        self.tesseract_cmd = tesseract_cmd
        self.lang = lang
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def check_available(self) -> str:
        """Return the Tesseract version, or raise if the executable or a language is missing."""
        try:
            version = str(pytesseract.get_tesseract_version())
            installed = set(pytesseract.get_languages(config=""))
        except (pytesseract.TesseractNotFoundError, OSError) as exc:
            raise OcrUnavailableError(
                "Tesseract executable not found. Install it and set TESSERACT_CMD in .env"
            ) from exc
        missing = [lang for lang in self.lang.split("+") if lang not in installed]
        if missing:
            raise OcrUnavailableError(f"Tesseract language data not installed: {', '.join(missing)}")
        return version

    def image_to_text(self, image: Image) -> OcrResult:
        text = pytesseract.image_to_string(image, lang=self.lang)
        data = pytesseract.image_to_data(image, lang=self.lang, output_type=pytesseract.Output.DICT)
        confidences = [
            float(conf) for word, conf in zip(data["text"], data["conf"]) if word.strip() and float(conf) >= 0
        ]
        return OcrResult(
            text=text,
            mean_confidence=sum(confidences) / len(confidences) if confidences else None,
            word_count=len(confidences),
            low_confidence_words=sum(1 for conf in confidences if conf < LOW_CONFIDENCE_THRESHOLD),
        )
