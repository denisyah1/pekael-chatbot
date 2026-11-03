"""Build the FAISS knowledge base from the approved PDF pages (Sprint 3, spec §4.1).

Calls the Gemini embedding API once per batch of 50 chunks. The new index version is used
only after it reloads correctly, a failed build keeps the previous one.

Usage from the project root:
    .venv\\Scripts\\python.exe scripts\\build_knowledge_base.py [pdf]
"""

import argparse
import sys
import time
from pathlib import Path

from pekael.config.app_configurator import AppConfigurator
from pekael.config.logging_config import configure_logging
from pekael.config.settings import ConfigError
from pekael.loaders.pdf_loader import DocumentLoadError
from pekael.models.embeddings import EmbeddingError
from pekael.services.ocr_service import OcrService, OcrUnavailableError
from pekael.vectorstores.base import VectorStoreError


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("pdf", nargs="?", help="PDF path (default: KNOWLEDGE_BASE_PATH)")
    args = parser.parse_args()

    try:
        config = AppConfigurator.read_config()
        configure_logging(config.log_level, config.secret_values())
        OcrService(config.tesseract_cmd, config.tesseract_lang).check_available()
        manager = AppConfigurator.create_manager_from_config(config)
    except (ConfigError, OcrUnavailableError, EmbeddingError) as exc:
        print(exc)
        return 2

    pdf_path = Path(args.pdf or config.knowledge_base_path)
    print(f"Membangun knowledge base dari {pdf_path.name}, halaman {config.knowledge_base_pages or 'semua'}")
    started = time.perf_counter()
    try:
        report = manager.initialize_knowledge_base(pdf_path)
    except (DocumentLoadError, VectorStoreError, EmbeddingError) as exc:
        print(f"Gagal, knowledge base lama tetap dipakai: {exc}")
        return 1

    indexing = report.indexing
    print(f"Selesai dalam {time.perf_counter() - started:.1f} s")
    print(f"  sumber      : {report.source_file} (sha256 {report.source_hash[:12]})")
    print(f"  halaman     : {report.page_count} (teks digital {report.native_pages}, OCR {report.ocr_pages})")
    print(f"  potongan    : {report.chunk_count}")
    print(f"  build_id    : {indexing.build_id}")
    print(f"  embedding   : {indexing.embedding_model}, {indexing.dimension} dimensi")
    print(f"  lokasi      : {indexing.index_path}")
    for warning in report.warnings:
        print(f"  peringatan  : {warning}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
