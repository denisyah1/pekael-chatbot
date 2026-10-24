"""Environment smoke tests (Setup step 5): verify core dependencies work without any API call."""

import os
import shutil
from pathlib import Path

import pytest

WINDOWS_TESSERACT = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")


def _tesseract_cmd() -> str | None:
    configured = os.getenv("TESSERACT_CMD")
    if configured:
        return configured
    found = shutil.which("tesseract")
    if found:
        return found
    return str(WINDOWS_TESSERACT) if WINDOWS_TESSERACT.exists() else None


def test_core_imports():
    import dotenv  # noqa: F401
    import faiss  # noqa: F401
    import langchain_core  # noqa: F401
    import langchain_google_genai  # noqa: F401
    import pydantic  # noqa: F401
    import pymupdf  # noqa: F401
    import pytesseract  # noqa: F401
    import streamlit  # noqa: F401
    from langchain_community.vectorstores import FAISS  # noqa: F401
    from langchain_text_splitters import RecursiveCharacterTextSplitter  # noqa: F401


def test_runtime_does_not_import_evaluator_packages():
    import sys

    import pekael  # noqa: F401

    assert "ragas" not in sys.modules
    assert "langchain_openai" not in sys.modules


def test_evaluation_packages_import_when_installed():
    """Guards the langchain-community pin: ragas fails to import with 0.4.2 (D-16)."""
    pytest.importorskip("ragas", reason="evaluation dependencies (requirements-eval.txt) not installed")
    from ragas.embeddings import GoogleEmbeddings  # noqa: F401
    from ragas.llms import llm_factory  # noqa: F401
    from ragas.metrics.collections import AnswerRelevancy, ContextRecall, Faithfulness  # noqa: F401


def test_faiss_flat_l2_save_and_load(tmp_path):
    import faiss
    from langchain_community.vectorstores import FAISS
    from langchain_core.embeddings import DeterministicFakeEmbedding

    embeddings = DeterministicFakeEmbedding(size=768)
    texts = ["syarat pendaftaran PKL", "jadwal seminar PKL", "laporan akhir PKL"]
    metadatas = [{"page": i + 1} for i in range(len(texts))]

    store = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
    assert isinstance(store.index, faiss.IndexFlatL2)
    assert store.index.d == 768

    store.save_local(str(tmp_path))
    reloaded = FAISS.load_local(str(tmp_path), embeddings, allow_dangerous_deserialization=True)

    doc, distance = reloaded.similarity_search_with_score("jadwal seminar PKL", k=1)[0]
    assert doc.metadata["page"] == 2
    assert distance == pytest.approx(0.0, abs=1e-4)


def test_pymupdf_extracts_text_and_renders_page():
    import pymupdf

    pdf = pymupdf.open()
    page = pdf.new_page()
    page.insert_text((72, 72), "Buku Panduan PKL", fontsize=14)

    assert "Buku Panduan PKL" in pdf[0].get_text()
    pixmap = pdf[0].get_pixmap(dpi=150)
    assert pixmap.width > 0 and pixmap.height > 0


def test_tesseract_ocr_indonesian():
    import pymupdf
    import pytesseract
    from PIL import Image

    cmd = _tesseract_cmd()
    if cmd is None:
        pytest.skip("Tesseract executable not found; set TESSERACT_CMD")
    pytesseract.pytesseract.tesseract_cmd = cmd

    assert "ind" in pytesseract.get_languages(config="")

    pdf = pymupdf.open()
    page = pdf.new_page()
    page.insert_text((72, 120), "PRAKTIK KERJA LAPANGAN", fontsize=28)
    pixmap = page.get_pixmap(dpi=200)
    image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)

    text = pytesseract.image_to_string(image, lang="ind+eng")
    assert "PRAKTIK" in text.upper()
