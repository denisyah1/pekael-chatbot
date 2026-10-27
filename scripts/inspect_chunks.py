"""Split the knowledge base with one or more chunk settings and report chunk statistics (Sprint 2).

No API calls. Writes data/processed/<pdf name>/chunks_<size>_<overlap>.jsonl (git-ignored).

Usage from the project root:
    .venv\\Scripts\\python.exe scripts\\inspect_chunks.py [--pages 4-16] [--configs 500:50,1000:150]
"""

import argparse
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

from pekael.config.app_configurator import AppConfigurator
from pekael.config.settings import ConfigError
from pekael.loaders.pdf_loader import DocumentLoadError, PDFLoader, parse_page_ranges
from pekael.services.ocr_service import OcrService, OcrUnavailableError
from pekael.splitters.recursive_character_splitter import RecursiveCharacterSplitter


def _configs(spec: str | None, default: tuple[int, int]) -> list[tuple[int, int]]:
    if not spec:
        return [default]
    pairs = []
    for item in spec.split(","):
        size, _, overlap = item.partition(":")
        pairs.append((int(size), int(overlap or 0)))
    return pairs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("pdf", nargs="?", help="PDF path (default: KNOWLEDGE_BASE_PATH)")
    parser.add_argument("--pages", help="page ranges, e.g. 4-16 (default: KNOWLEDGE_BASE_PAGES)")
    parser.add_argument("--configs", help="chunk_size:chunk_overlap list (default: CHUNK_SIZE:CHUNK_OVERLAP)")
    args = parser.parse_args()

    try:
        config = AppConfigurator.read_config()
        pages = parse_page_ranges(args.pages if args.pages is not None else config.knowledge_base_pages)
    except (ConfigError, ValueError) as exc:
        print(exc)
        return 2
    pdf_path = Path(args.pdf or config.knowledge_base_path)
    ocr = OcrService(config.tesseract_cmd, config.tesseract_lang)
    try:
        ocr.check_available()
        loader = PDFLoader(
            ocr,
            min_text_chars=config.ocr_min_text_chars_per_page,
            ocr_dpi=config.ocr_render_dpi,
            corrections_dir=config.ocr_corrections_path,
            pages=pages,
        )
        documents = loader.load(pdf_path)
    except (OcrUnavailableError, DocumentLoadError) as exc:
        print(exc)
        return 2

    corrected = [d.metadata["page"] for d in documents if d.metadata.get("manually_corrected")]
    print(f"{pdf_path.name}: {len(documents)} halaman dimuat {[d.metadata['page'] for d in documents]}")
    print(f"koreksi manual: {corrected}\n")
    out_dir = Path("data/processed") / pdf_path.stem
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"{'size:overlap':>12} {'chunks':>6} {'min':>5} {'mean':>6} {'max':>5} {'per hal.':>8} {'tanpa bagian':>12} {'duplikat':>8}")
    for size, overlap in _configs(args.configs, (config.chunk_size, config.chunk_overlap)):
        chunks = RecursiveCharacterSplitter(size, overlap).split(documents)
        lengths = [len(c.page_content) for c in chunks]
        duplicates = sum(n - 1 for n in Counter(c.page_content for c in chunks).values() if n > 1)
        no_section = sum(1 for c in chunks if not c.metadata["section"])
        print(
            f"{size:>7}:{overlap:<4} {len(chunks):>6} {min(lengths):>5} {statistics.mean(lengths):>6.0f} {max(lengths):>5} "
            f"{len(chunks) / len(documents):>8.1f} {no_section:>12} {duplicates:>8}"
        )
        target = out_dir / f"chunks_{size}_{overlap}.jsonl"
        with target.open("w", encoding="utf-8") as handle:
            for chunk in chunks:
                handle.write(json.dumps({"text": chunk.page_content, "metadata": chunk.metadata}, ensure_ascii=False) + "\n")
    print(f"\nChunks written to {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
