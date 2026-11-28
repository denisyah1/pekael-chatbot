"""Ragas evaluation of Pekael on the ground truth dataset (spec §10.3, FR-11, SUP-03).

For every selected question: Pekael answers it through the normal chain (no answer cache), the
retrieved chunks and the answer are kept, then Faithfulness, Answer Relevancy and Context Recall
are scored by the Groq evaluator LLM with Gemini embeddings (D-52). Each metric's intermediate
results are saved with its score. Rows are written as they finish, ``--resume`` continues a run
that stopped (for example on the Groq daily limit) without asking Pekael or Groq again.

Calls per question: Gemini once (answer), one embedding for retrieval, Groq about 6 times
(2 Faithfulness, 3 Answer Relevancy, 1 Context Recall) and Gemini embeddings once for Answer
Relevancy. Never run automatically. Usage from the project root:

    .venv\\Scripts\\python.exe scripts\\run_ragas_evaluation.py --experiment EXP-012 [--scope uji36] [--ids 1,12] [--pause 20] [--resume]
"""

import argparse
import asyncio
import csv
import json
import statistics
import sys
import time
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

from pekael.config.app_configurator import AppConfigurator
from pekael.config.logging_config import configure_logging
from pekael.config.settings import ConfigError
from pekael.core.schemas import ChainState
from pekael.evaluation.dataset import load_dataset, select
from pekael.evaluation.ragas_evaluator import METRICS, RagasEvaluator

RESULTS = Path("data/evaluation/results")
DAILY_LIMIT = "tokens per day"  # Groq free tier: 200000 tokens per day for openai/gpt-oss-120b
PACKAGES = ("ragas", "openai", "langchain-core", "langchain-google-genai", "google-genai", "faiss-cpu")


def answer(manager, question: str) -> dict:
    """Ask Pekael like a student, keeping what the metrics need."""
    started = time.perf_counter()
    state = manager.chain.invoke(ChainState(question=question))
    response = state.response
    return {
        "response": response.answer,
        "status": response.status.value,
        "retrieved_contexts": [r.document.page_content for r in state.retrieved],
        "retrieved_sources": [{"source_file": r.document.metadata.get("source_file"), "page": r.document.metadata.get("page"),
                               "distance": round(r.distance, 4)} for r in state.retrieved],
        "cited_sources": [{"source_file": s.source_file, "page": s.page} for s in response.sources],
        "answer_seconds": round(time.perf_counter() - started, 2),
    }


def summarise(rows: list[dict]) -> dict:
    summary = {}
    for metric in METRICS:
        values = [r["metrics"][metric]["score"] for r in rows if r["metrics"][metric]["score"] is not None]
        summary[metric] = {
            "mean": round(statistics.fmean(values), 4) if values else None,
            "median": round(statistics.median(values), 4) if values else None,
            "min": round(min(values), 4) if values else None,
            "scored": len(values),
            "failed": len(rows) - len(values),
        }
    return summary


async def run(args) -> int:
    try:
        config = AppConfigurator.read_config()
    except ConfigError as exc:
        print(exc)
        return 2
    missing = [n for n, v in (("GROQ_API_KEY", config.groq_api_key), ("GEMINI_API_KEY", config.gemini_api_key)) if not v]
    if missing:
        print("Variabel berikut belum diisi di .env:", ", ".join(missing))
        return 2
    configure_logging("WARNING", config.secret_values())

    entries = select(load_dataset(config.ragas_dataset_path), args.scope, args.ids.split(",") if args.ids else None)
    entries = [e for e in entries if e.category == "pkl"]  # redirect and non-PKL questions are checked by status (D-57)
    folder = RESULTS / args.experiment
    folder.mkdir(parents=True, exist_ok=True)
    rows_file = folder / "rows.jsonl"
    done, retry = {}, {}
    if args.resume and rows_file.is_file():
        for r in map(json.loads, rows_file.read_text(encoding="utf-8").splitlines()):
            # a later line for the same id replaces an earlier one, rows with a failed metric are scored again
            if any(r["metrics"][m]["error"] for m in METRICS):
                retry[r["id"]] = r
                done.pop(r["id"], None)
            else:
                done[r["id"]] = r
                retry.pop(r["id"], None)
    elif rows_file.exists():
        print(f"{rows_file} sudah ada. Pakai --resume untuk melanjutkan atau nama --experiment lain.")
        return 2

    manager = AppConfigurator.create_manager_from_config(config)
    manager.vector_store.load()
    manifest = manager.vector_store.manifest
    evaluator = RagasEvaluator(
        config.groq_api_key.get_secret_value(), config.groq_eval_model, config.groq_base_url,
        config.gemini_api_key.get_secret_value(), config.gemini_embedding_model,
    )
    dataset_version = entries[0].version if entries else "?"
    print(f"{args.experiment}: {len(entries)} pertanyaan (dataset {dataset_version}), indeks {manifest['build_id']}, "
          f"jawaban {config.gemini_chat_model}, evaluator {config.groq_eval_model} (Groq), embedding {config.gemini_embedding_model}")

    started_all = time.perf_counter()
    with rows_file.open("a", encoding="utf-8") as out:
        for number, entry in enumerate(entries, start=1):
            if entry.id in done:
                continue
            if entry.id in retry:  # keep the answer that was already given, only the scoring failed
                pekael = {k: retry[entry.id][k] for k in ("response", "status", "retrieved_contexts", "retrieved_sources",
                                                          "cited_sources", "answer_seconds")}
            else:
                pekael = answer(manager, entry.user_input)
            if pekael["retrieved_contexts"]:
                outcomes = await evaluator.score(entry.user_input, pekael["response"], pekael["retrieved_contexts"], entry.reference)
                metrics = {name: {"score": o.score, "seconds": o.seconds, "details": o.details, "error": o.error} for name, o in outcomes.items()}
            else:
                metrics = {name: {"score": None, "seconds": 0, "details": {}, "error": "no retrieved contexts"} for name in METRICS}
            row = {"id": entry.id, "topic": entry.topic, "question_type": entry.question_type, "user_input": entry.user_input,
                   "reference": entry.reference, **pekael, "metrics": metrics}
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
            out.flush()
            if any(metrics[m]["error"] for m in METRICS):
                retry[entry.id] = row
            else:
                done[entry.id] = row
                retry.pop(entry.id, None)
            shown = "  ".join(f"{m[:5]} {metrics[m]['score']:.3f}" if metrics[m]["score"] is not None else f"{m[:5]} gagal" for m in METRICS)
            print(f"[{number:>2}/{len(entries)}] {entry.id:>3} {pekael['status']:>12}  {shown}", flush=True)
            for m in METRICS:
                if metrics[m]["error"]:
                    print(f"         {m}: {metrics[m]['error']}", flush=True)
            if any(DAILY_LIMIT in (metrics[m]["error"] or "") for m in METRICS):
                print("Batas token harian Groq tercapai. Jalankan lagi dengan --resume setelah kuota pulih.", flush=True)
                break
            await asyncio.sleep(args.pause)

    # one line per id: complete rows first chosen, failed ones kept so --resume can score them later
    final = {**retry, **done}
    rows_file.write_text("".join(json.dumps(final[e.id], ensure_ascii=False) + "\n" for e in entries if e.id in final), encoding="utf-8")
    rows = [done[e.id] for e in entries if e.id in done]
    if retry:
        print(f"{len(retry)} pertanyaan belum dinilai lengkap: {', '.join(e.id for e in entries if e.id in retry)}")
    summary = {
        "experiment": args.experiment,
        "finished_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "minutes": round((time.perf_counter() - started_all) / 60, 1),
        "questions": len(rows),
        "dataset": {"path": str(config.ragas_dataset_path), "version": dataset_version, "scope": args.scope, "ids": [r["id"] for r in rows]},
        "pekael": {"build_id": manifest["build_id"], "documents": [s["source_file"] for s in manifest.get("sources", [])],
                   "chat_model": config.gemini_chat_model, "embedding_model": config.gemini_embedding_model,
                   "dimension": config.embedding_output_dimension, "chunk_size": config.chunk_size, "chunk_overlap": config.chunk_overlap,
                   "k": config.retrieval_k, "max_l2_distance": config.retrieval_max_l2_distance},
        "evaluator": {"llm": config.groq_eval_model, "provider": "Groq (OpenAI-compatible API)",
                      "embeddings": config.gemini_embedding_model, "answer_relevancy_strictness": 3},
        "packages": {p: version(p) for p in PACKAGES},
        "metrics": summarise(rows),
    }
    (folder / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    with (folder / "scores.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["id", "status", *METRICS, "answer_seconds"])
        for r in rows:
            writer.writerow([r["id"], r["status"], *[r["metrics"][m]["score"] for m in METRICS], r["answer_seconds"]])
    print()
    for metric, values in summary["metrics"].items():
        print(f"{metric:>17}: rerata {values['mean']}  median {values['median']}  min {values['min']}  ({values['scored']} dinilai, {values['failed']} gagal)")
    print(f"Hasil: {folder}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--experiment", required=True, help="result folder name under data/evaluation/results, e.g. EXP-012")
    parser.add_argument("--scope", default="uji36", choices=("uji36", "pkl", "all"), help="uji36: 36 test questions of Sprint 4")
    parser.add_argument("--ids", help="comma-separated ids instead of --scope, e.g. 1,12,E6")
    parser.add_argument("--pause", type=float, default=20.0, help="seconds between questions (Groq free tier: 8000 tokens per minute)")
    parser.add_argument("--resume", action="store_true", help="continue a stopped run in the same folder")
    return asyncio.run(run(parser.parse_args()))


if __name__ == "__main__":
    sys.exit(main())
