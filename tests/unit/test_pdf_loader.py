import hashlib

import pymupdf
import pytest

from pekael.loaders.factory import DocumentLoaderFactory
from pekael.loaders.pdf_loader import NATIVE_TEXT, TESSERACT_OCR, DocumentLoadError, PDFLoader
from pekael.services.ocr_service import OcrResult

NATIVE_PAGE = "Mahasiswa wajib mengikuti pembekalan sebelum melaksanakan PKL di instansi mitra."


class FakeOcr:
    """Stands in for Tesseract so unit tests do not need the executable."""

    def __init__(self, text: str = "Teks hasil OCR halaman scan.") -> None:
        self.text = text
        self.calls = 0

    def image_to_text(self, image) -> OcrResult:
        self.calls += 1
        assert image.mode == "L" and image.width > 0
        return OcrResult(self.text, mean_confidence=91.5, word_count=5, low_confidence_words=1)


def _make_pdf(path, pages: list[str | None]):
    """Create a PDF where a string page has a text layer and None is an image-only (scanned) page."""
    pdf = pymupdf.open()
    for content in pages:
        page = pdf.new_page()
        if content is not None:
            page.insert_textbox(pymupdf.Rect(50, 50, 550, 800), content, fontsize=11)
        else:
            pixmap = pymupdf.Pixmap(pymupdf.csGRAY, pymupdf.IRect(0, 0, 200, 100), False)
            pixmap.set_rect(pixmap.irect, (255,))
            page.insert_image(pymupdf.Rect(50, 50, 250, 150), pixmap=pixmap)
    pdf.save(path)
    pdf.close()
    return path


def test_native_and_scanned_pages_use_the_right_method(tmp_path):
    path = _make_pdf(tmp_path / "pedoman.pdf", [NATIVE_PAGE, None, NATIVE_PAGE])
    ocr = FakeOcr()

    documents = PDFLoader(ocr, min_text_chars=40).load(path)

    assert [d.metadata["page"] for d in documents] == [1, 2, 3]
    assert [d.metadata["extraction_method"] for d in documents] == [NATIVE_TEXT, TESSERACT_OCR, NATIVE_TEXT]
    assert ocr.calls == 1
    assert documents[0].page_content == NATIVE_PAGE
    assert documents[1].page_content == "Teks hasil OCR halaman scan."


def test_metadata_identifies_the_source(tmp_path):
    path = _make_pdf(tmp_path / "pedoman.pdf", [NATIVE_PAGE, None])
    expected_hash = hashlib.sha256(path.read_bytes()).hexdigest()

    native, scanned = PDFLoader(FakeOcr()).load(path)

    for document in (native, scanned):
        assert document.metadata["source_file"] == "pedoman.pdf"
        assert document.metadata["source_hash"] == expected_hash
        assert document.metadata["total_pages"] == 2
    assert "ocr_mean_confidence" not in native.metadata
    assert scanned.metadata["ocr_mean_confidence"] == 91.5
    assert scanned.metadata["ocr_low_confidence_words"] == 1


def test_short_text_layer_falls_back_to_ocr(tmp_path):
    path = _make_pdf(tmp_path / "short.pdf", ["12"])
    ocr = FakeOcr()

    (document,) = PDFLoader(ocr, min_text_chars=40).load(path)

    assert document.metadata["extraction_method"] == TESSERACT_OCR
    assert ocr.calls == 1


def test_scanned_page_without_ocr_service_is_an_error(tmp_path):
    path = _make_pdf(tmp_path / "scan.pdf", [None])

    with pytest.raises(DocumentLoadError, match="OCR is not configured"):
        PDFLoader(ocr_service=None).load(path)


def test_ocr_text_is_cleaned(tmp_path):
    path = _make_pdf(tmp_path / "scan.pdf", [None])

    (document,) = PDFLoader(FakeOcr("baris satu\nbaris  dua\n\n\n")).load(path)

    assert document.page_content == "baris satu baris dua"


def test_missing_file(tmp_path):
    with pytest.raises(DocumentLoadError, match="File not found"):
        PDFLoader().load(tmp_path / "nothing.pdf")


def test_non_pdf_file_is_rejected(tmp_path):
    fake = tmp_path / "notes.pdf"
    fake.write_text("ini bukan PDF", encoding="utf-8")

    with pytest.raises(DocumentLoadError, match="Not a readable PDF"):
        PDFLoader().load(fake)


def test_password_protected_pdf_is_rejected(tmp_path):
    path = tmp_path / "locked.pdf"
    pdf = pymupdf.open()
    pdf.new_page().insert_text((72, 72), NATIVE_PAGE)
    pdf.save(path, encryption=pymupdf.PDF_ENCRYPT_AES_256, user_pw="rahasia", owner_pw="rahasia")
    pdf.close()

    with pytest.raises(DocumentLoadError, match="password"):
        PDFLoader().load(path)


def test_factory_passes_ocr_settings(tmp_path):
    loader = DocumentLoaderFactory.get_loader("pdf", ocr_service=FakeOcr(), min_text_chars=10, ocr_dpi=150)

    assert isinstance(loader, PDFLoader)
    assert (loader.min_text_chars, loader.ocr_dpi) == (10, 150)


@pytest.mark.parametrize(("chars", "dpi"), [(-1, 200), (40, 0)])
def test_invalid_parameters(chars, dpi):
    with pytest.raises(ValueError):
        PDFLoader(min_text_chars=chars, ocr_dpi=dpi)
