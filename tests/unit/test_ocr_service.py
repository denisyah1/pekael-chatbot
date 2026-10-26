import os
import shutil
from pathlib import Path

import pymupdf
import pytest
from PIL import Image

from pekael.services.ocr_service import OcrService, OcrUnavailableError

WINDOWS_TESSERACT = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")


def _tesseract_cmd() -> str | None:
    if os.getenv("TESSERACT_CMD"):
        return os.environ["TESSERACT_CMD"]
    if shutil.which("tesseract"):
        return shutil.which("tesseract")
    return str(WINDOWS_TESSERACT) if WINDOWS_TESSERACT.exists() else None


@pytest.fixture
def restore_tesseract_cmd():
    import pytesseract

    original = pytesseract.pytesseract.tesseract_cmd
    yield
    pytesseract.pytesseract.tesseract_cmd = original


def _rendered_text_image(text: str) -> Image.Image:
    pdf = pymupdf.open()
    page = pdf.new_page()
    page.insert_text((72, 120), text, fontsize=24)
    pixmap = page.get_pixmap(dpi=200, colorspace=pymupdf.csGRAY)
    return Image.frombytes("L", (pixmap.width, pixmap.height), pixmap.samples)


def test_configured_path_is_used(restore_tesseract_cmd):
    import pytesseract

    OcrService(tesseract_cmd=r"D:\tools\tesseract.exe")

    assert pytesseract.pytesseract.tesseract_cmd == r"D:\tools\tesseract.exe"


def test_missing_executable_is_reported(tmp_path, restore_tesseract_cmd):
    service = OcrService(tesseract_cmd=str(tmp_path / "no-tesseract.exe"))

    with pytest.raises(OcrUnavailableError, match="TESSERACT_CMD"):
        service.check_available()


def test_real_tesseract_reads_indonesian_text(restore_tesseract_cmd):
    cmd = _tesseract_cmd()
    if cmd is None:
        pytest.skip("Tesseract executable not found; set TESSERACT_CMD")
    service = OcrService(tesseract_cmd=cmd, lang="ind+eng")
    service.check_available()

    result = service.image_to_text(_rendered_text_image("Pembekalan PKL wajib diikuti"))

    assert "Pembekalan" in result.text and "wajib" in result.text
    assert result.word_count >= 4
    assert result.mean_confidence is not None and result.mean_confidence > 50


def test_missing_language_is_reported(restore_tesseract_cmd):
    cmd = _tesseract_cmd()
    if cmd is None:
        pytest.skip("Tesseract executable not found; set TESSERACT_CMD")

    with pytest.raises(OcrUnavailableError, match="xyz"):
        OcrService(tesseract_cmd=cmd, lang="ind+xyz").check_available()
