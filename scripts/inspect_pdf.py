"""Extract a PDF page by page and write an extraction report (spec §4.1 steps 3-6, Sprint 1).

Writes to data/processed/<pdf name>/ (git-ignored):
    page_NNN.txt      cleaned text used by the knowledge base
    page_NNN.raw.txt  text before clean-up (native text or raw OCR output)
    report.json       per-page statistics
    report.md         human-readable report for manual OCR review

Usage from the project root:
    .venv\\Scripts\\python.exe scripts\\inspect_pdf.py [PDF] [--dpi 300] [--pages 1-5]
"""

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pymupdf

from pekael import __version__
from pekael.config.app_configurator import AppConfigurator
from pekael.config.settings import ConfigError
from pekael.loaders.pdf_loader import DocumentLoadError, PDFLoader, file_sha256
from pekael.services.ocr_service import OcrService, OcrUnavailableError

# Pages whose mean OCR confidence is below this are listed first for manual review.
REVIEW_CONFIDENCE = 85


def _page_range(spec: str | None, total: int) -> list[int]:
    if not spec:
        return list(range(1, total + 1))
    start, _, end = spec.partition("-")
    first, last = int(start), int(end or start)
    if not 1 <= first <= last <= total:
        raise SystemExit(f"--pages must be within 1-{total}")
    return list(range(first, last + 1))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("pdf", nargs="?", help="PDF path (default: KNOWLEDGE_BASE_PATH)")
    parser.add_argument("--dpi", type=int, help="OCR render resolution (default: OCR_RENDER_DPI)")
    parser.add_argument("--pages", help="page range, e.g. 3 or 1-5 (default: all)")
    parser.add_argument("--out", help="output folder (default: data/processed/<pdf name>)")
    args = parser.parse_args()

    try:
        config = AppConfigurator.read_config()
    except ConfigError as exc:
        print(exc)
        return 2
    pdf_path = Path(args.pdf or config.knowledge_base_path)
    dpi = args.dpi or config.ocr_render_dpi
    out_dir = Path(args.out or Path("data/processed") / pdf_path.stem)

    ocr = OcrService(config.tesseract_cmd, config.tesseract_lang)
    try:
        tesseract_version = ocr.check_available()
    except OcrUnavailableError as exc:
        print(exc)
        return 2
    loader = PDFLoader(ocr, min_text_chars=config.ocr_min_text_chars_per_page, ocr_dpi=dpi)

    try:
        pdf = loader.open_pdf(pdf_path)
    except DocumentLoadError as exc:
        print(exc)
        return 2
    out_dir.mkdir(parents=True, exist_ok=True)
    source_hash = file_sha256(pdf_path)
    pages = _page_range(args.pages, pdf.page_count)

    rows = []
    for number in pages:
        page = pdf[number - 1]
        start = time.perf_counter()
        extraction = loader.extract_page(page)
        elapsed = time.perf_counter() - start
        document = loader.to_document(extraction, pdf_path.name, source_hash, pdf.page_count)
        meta = document.metadata
        (out_dir / f"page_{number:03d}.raw.txt").write_text(extraction.raw_text, encoding="utf-8")
        (out_dir / f"page_{number:03d}.txt").write_text(document.page_content, encoding="utf-8")
        rows.append(
            {
                "page": number,
                "extraction_method": meta["extraction_method"],
                "native_text_chars": len(page.get_text().strip()),
                "clean_chars": len(document.page_content),
                "ocr_mean_confidence": round(meta["ocr_mean_confidence"], 1)
                if meta.get("ocr_mean_confidence") is not None
                else None,
                "ocr_low_confidence_words": meta.get("ocr_low_confidence_words"),
                "seconds": round(elapsed, 2),
            }
        )
        print(f"page {number:>3}: {rows[-1]['extraction_method']:<14} {rows[-1]['clean_chars']:>5} chars  "
              f"conf={rows[-1]['ocr_mean_confidence']}  low={rows[-1]['ocr_low_confidence_words']}  {elapsed:.1f}s")
    pdf.close()

    report = {
        "source_file": pdf_path.name,
        "source_sha256": source_hash,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "pekael_version": __version__,
        "tesseract_version": tesseract_version,
        "tesseract_lang": config.tesseract_lang,
        "ocr_render_dpi": dpi,
        "ocr_min_text_chars_per_page": config.ocr_min_text_chars_per_page,
        "pages": rows,
    }
    (out_dir / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    (out_dir / "report.md").write_text(_markdown(report), encoding="utf-8")
    print(f"\nReport written to {out_dir}")
    return 0


def _markdown(report: dict) -> str:
    rows = report["pages"]
    ocr_rows = [r for r in rows if r["ocr_mean_confidence"] is not None]
    review_first = sorted(
        (r for r in ocr_rows if r["ocr_mean_confidence"] < REVIEW_CONFIDENCE), key=lambda r: r["ocr_mean_confidence"]
    )
    lines = [
        f"# Laporan Ekstraksi — {report['source_file']}",
        "",
        f"- SHA-256: `{report['source_sha256']}`",
        f"- Dibuat: {report['generated_at']} (pekael {report['pekael_version']})",
        f"- Tesseract {report['tesseract_version']}, bahasa `{report['tesseract_lang']}`, render {report['ocr_render_dpi']} dpi",
        f"- Halaman diproses: {len(rows)} (teks digital: {len(rows) - len(ocr_rows)}, OCR: {len(ocr_rows)})",
        "",
        f"## Prioritas pemeriksaan manual (keyakinan OCR < {REVIEW_CONFIDENCE})",
        "",
        ", ".join(f"hal. {r['page']} ({r['ocr_mean_confidence']})" for r in review_first) or "Tidak ada.",
        "",
        "## Per halaman",
        "",
        "| Hal. | Metode | Karakter | Keyakinan OCR | Kata ragu (<60) | Detik |",
        "|---|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['page']} | {r['extraction_method']} | {r['clean_chars']} | {r['ocr_mean_confidence'] or '-'} "
            f"| {r['ocr_low_confidence_words'] if r['ocr_low_confidence_words'] is not None else '-'} | {r['seconds']} |"
        )
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    sys.exit(main())
