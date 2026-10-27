"""EXP-002: compare chunk size/overlap (and L2 normalisation) on sample questions (Sprint 2).

Uses the sample questions of docs/scrum/sprint-01/topik_pertanyaan.md. A question counts as a
hit when a retrieved chunk comes from one of the pages listed for it. This is a development
proxy, not the research evaluation (Ragas, Sprint 6).

Calls the Gemini embedding API (each distinct text once, results cached in memory).
Usage from the project root:
    .venv\\Scripts\\python.exe scripts\\run_chunk_experiment.py data\\source\\Pedoman-PKL-2025.pdf --pages 4-16
"""

import argparse
import json
import re
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import faiss
import numpy as np

from pekael.config.app_configurator import AppConfigurator
from pekael.loaders.pdf_loader import PDFLoader, parse_page_ranges
from pekael.models.embeddings import GeminiEmbeddings, build_embeddings, l2_normalize
from pekael.services.ocr_service import OcrService
from pekael.splitters.recursive_character_splitter import RecursiveCharacterSplitter

TOPICS = Path("docs/scrum/sprint-01/topik_pertanyaan.md")
VARIANTS = [(500, 50, True), (800, 100, True), (1000, 150, True), (1500, 200, True), (1000, 150, False)]


def load_questions(path: Path) -> tuple[list[dict], list[dict]]:
    """In-scope questions with expected pages, and out-of-scope questions."""
    in_scope, out_scope = [], []
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 5 and cells[0].isdigit():
            pages = sorted({p for part in re.findall(r"\d+(?:–\d+)?", cells[2]) for p in _expand(part)})
            in_scope.append({"id": cells[0], "question": cells[3], "pages": pages})
        elif len(cells) >= 2 and re.fullmatch(r"[LN]\d+", cells[0]):
            out_scope.append({"id": cells[0], "question": cells[1]})
    return in_scope, out_scope


def _expand(part: str) -> range:
    first, _, last = part.partition("–")
    return range(int(first), int(last or first) + 1)


class CachedRawEmbeddings:
    """Fetch each distinct text once (unnormalised), so variants differ only in local processing."""

    def __init__(self, embeddings: GeminiEmbeddings) -> None:
        self._embeddings = embeddings
        self._documents: dict[str, list[float]] = {}
        self._queries: dict[str, list[float]] = {}
        self.api_texts = 0

    def documents(self, texts: list[str]) -> list[list[float]]:
        missing = list(dict.fromkeys(t for t in texts if t not in self._documents))
        if missing:
            for text, vector in zip(missing, self._embeddings.embed_documents(missing)):
                self._documents[text] = vector
            self.api_texts += len(missing)
        return [self._documents[t] for t in texts]

    def query(self, text: str) -> list[float]:
        if text not in self._queries:
            self._queries[text] = self._embeddings.embed_query(text)
            self.api_texts += 1
        return self._queries[text]


def evaluate(chunks, cache, in_scope, out_scope, normalize: bool, k: int) -> dict:
    prepare = l2_normalize if normalize else list
    matrix = np.array([prepare(v) for v in cache.documents([c.page_content for c in chunks])], dtype="float32")
    index = faiss.IndexFlatL2(matrix.shape[1])
    index.add(matrix)

    def search(question: str):
        distances, ids = index.search(np.array([prepare(cache.query(question))], dtype="float32"), k)
        return [(float(d), chunks[i].metadata["page"], chunks[i].metadata["chunk_id"]) for d, i in zip(distances[0], ids[0])]

    rows, reciprocal = [], []
    for q in in_scope:
        results = search(q["question"])
        rank = next((r for r, (_, page, _) in enumerate(results, 1) if page in q["pages"]), None)
        reciprocal.append(1 / rank if rank else 0.0)
        rows.append({"id": q["id"], "expected_pages": q["pages"], "rank": rank, "top1_distance": results[0][0],
                     "retrieved": [{"page": p, "chunk_id": c, "distance": round(d, 4)} for d, p, c in results]})
    out_rows = [{"id": q["id"], "top1_distance": search(q["question"])[0][0]} for q in out_scope]
    in_top1 = [r["top1_distance"] for r in rows]
    out_top1 = [r["top1_distance"] for r in out_rows]
    return {
        "chunks": len(chunks),
        "hit_at_1": sum(r["rank"] == 1 for r in rows) / len(rows),
        f"hit_at_{k}": sum(r["rank"] is not None for r in rows) / len(rows),
        "mrr": statistics.mean(reciprocal),
        "in_scope_top1_distance": {"mean": statistics.mean(in_top1), "max": max(in_top1)},
        "out_of_scope_top1_distance": {"mean": statistics.mean(out_top1), "min": min(out_top1)},
        "misses": [r for r in rows if r["rank"] is None],
        "questions": rows,
        "out_of_scope": out_rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("pdf", nargs="?")
    parser.add_argument("--pages")
    args = parser.parse_args()

    config = AppConfigurator.read_config()
    pdf_path = Path(args.pdf or config.knowledge_base_path)
    pages = parse_page_ranges(args.pages if args.pages is not None else config.knowledge_base_pages)
    k = config.retrieval_k
    in_scope, out_scope = load_questions(TOPICS)
    print(f"Pertanyaan: {len(in_scope)} dalam cakupan, {len(out_scope)} di luar cakupan, k={k}")

    loader = PDFLoader(OcrService(config.tesseract_cmd, config.tesseract_lang), config.ocr_min_text_chars_per_page,
                       config.ocr_render_dpi, config.ocr_corrections_path, pages)
    documents = loader.load(pdf_path)
    print(f"Halaman dimuat: {[d.metadata['page'] for d in documents]}\n")

    cache = CachedRawEmbeddings(build_embeddings(config, normalize=False))
    started = time.perf_counter()
    results = []
    print(f"{'variant':>16} {'chunks':>6} {'hit@1':>6} {f'hit@{k}':>6} {'MRR':>6} {'d_in mean/max':>15} {'d_out mean/min':>15}")
    for size, overlap, normalize in VARIANTS:
        chunks = RecursiveCharacterSplitter(size, overlap).split(documents)
        result = evaluate(chunks, cache, in_scope, out_scope, normalize, k)
        result.update(chunk_size=size, chunk_overlap=overlap, normalized=normalize)
        results.append(result)
        name = f"{size}:{overlap}{'' if normalize else ' raw'}"
        din, dout = result["in_scope_top1_distance"], result["out_of_scope_top1_distance"]
        print(f"{name:>16} {result['chunks']:>6} {result['hit_at_1']:>6.2f} {result[f'hit_at_{k}']:>6.2f} {result['mrr']:>6.3f} "
              f"{din['mean']:>7.3f}/{din['max']:<7.3f} {dout['mean']:>7.3f}/{dout['min']:<7.3f}")
    elapsed = time.perf_counter() - started

    for result in results:
        if result["misses"]:
            ids = ", ".join(f"{m['id']} (hal. {m['expected_pages']} → {[r['page'] for r in m['retrieved']]})" for m in result["misses"])
            print(f"meleset {result['chunk_size']}:{result['chunk_overlap']}{'' if result['normalized'] else ' raw'}: {ids}")

    out = Path("data/processed") / pdf_path.stem / "exp002.json"
    out.write_text(json.dumps({
        "experiment": "EXP-002", "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "embedding_model": config.gemini_embedding_model, "dimension": config.embedding_output_dimension,
        "pages": [d.metadata["page"] for d in documents], "k": k, "api_texts": cache.api_texts,
        "seconds": round(elapsed, 1), "results": results,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nTeks dikirim ke API: {cache.api_texts}, waktu {elapsed:.1f} s. Hasil: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
