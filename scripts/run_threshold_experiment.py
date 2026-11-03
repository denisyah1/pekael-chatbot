"""EXP-004: initial calibration of RETRIEVAL_MAX_L2_DISTANCE on the active FAISS index (Sprint 3).

Questions: the sample questions of docs/scrum/sprint-01/topik_pertanyaan.md (pages 4-16) plus
EXTRA_IN_SCOPE for pages 22-28. Development data, not the Ragas dataset.

Rule fixed before the run (spec §2.5, §4.5): the initial threshold is the midpoint between the
largest nearest-chunk distance of an in-scope question and the smallest one of a non-PKL
question (N group), rounded to 2 decimals. PKL questions the handbook does not answer
(L group) are not expected to be separable by distance (EXP-002); with --generate they go
through the full pipeline to check that the prompt policy rejects them.

Calls the Gemini embedding API once per question, and with --generate also Gemini once per
question that passes the threshold.
Usage from the project root:
    .venv\\Scripts\\python.exe scripts\\run_threshold_experiment.py [--generate] [--pause 4]
"""

import argparse
import dataclasses
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from run_chunk_experiment import TOPICS, load_questions

from pekael.config.app_configurator import AppConfigurator
from pekael.config.logging_config import configure_logging
from pekael.core.rag_steps import RagSteps

EXTRA_IN_SCOPE = [
    {"id": "E1", "question": "Sistem rujukan pustaka apa yang dipakai dalam laporan PKL?", "pages": [22]},
    {"id": "E2", "question": "Apa saja isi Bab I Pendahuluan pada laporan PKL?", "pages": [23]},
    {"id": "E3", "question": "Dokumen apa saja yang harus dilampirkan pada laporan PKL?", "pages": [24]},
    {"id": "E4", "question": "Bagaimana contoh urutan sistematika laporan PKL?", "pages": [23, 25]},
    {"id": "E5", "question": "Aspek apa saja yang dinilai pada nilai sikap (N1)?", "pages": [27]},
    {"id": "E6", "question": "Bagaimana cara menghitung nilai akhir PKL?", "pages": [16, 28]},
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--generate", action="store_true", help="also answer every question with Gemini")
    parser.add_argument("--pause", type=float, default=4.0, help="seconds between Gemini calls (free-tier rate limit)")
    args = parser.parse_args()

    config = AppConfigurator.read_config()
    configure_logging("WARNING", config.secret_values())
    manager = AppConfigurator.create_manager_from_config(config)
    store, k = manager.vector_store, config.retrieval_k
    store.load()
    in_scope, out_scope = load_questions(TOPICS)
    in_scope += EXTRA_IN_SCOPE
    print(f"Indeks {store.active_build_id()}, k={k}, {len(in_scope)} dalam cakupan, {len(out_scope)} di luar cakupan")

    rows = []
    for q in in_scope + out_scope:
        retrieved = store.get_relevant_document(q["question"], k=k)
        pages = [r.document.metadata["page"] for r in retrieved]
        rank = next((i for i, p in enumerate(pages, 1) if p in q.get("pages", [])), None)
        group = "in" if "pages" in q else q["id"][0]
        rows.append({**q, "group": group, "nearest": retrieved[0].distance, "rank": rank,
                     "retrieved": [{"page": p, "distance": round(r.distance, 4)} for p, r in zip(pages, retrieved)]})

    in_max = max(r["nearest"] for r in rows if r["group"] == "in")
    n_min = min(r["nearest"] for r in rows if r["group"] == "N")
    threshold = round((in_max + n_min) / 2, 2)
    print(f"\n{'id':>4} {'kelompok':>8} {'jarak':>6} {'peringkat':>9}  halaman terambil")
    for r in sorted(rows, key=lambda r: r["nearest"]):
        mark = "" if r["nearest"] <= threshold else "  ditolak ambang"
        print(f"{r['id']:>4} {r['group']:>8} {r['nearest']:>6.3f} {str(r['rank'] or '-'):>9}  {[x['page'] for x in r['retrieved']]}{mark}")
    hit = sum(r["rank"] is not None for r in rows if r["group"] == "in")
    print(f"\nHit@{k}: {hit}/{len(in_scope)}. Jarak terbesar dalam cakupan {in_max:.3f}, terkecil non-PKL {n_min:.3f}")
    print(f"Ambang awal (titik tengah): {threshold:.2f}")
    for group in ("in", "L", "N"):
        members = [r for r in rows if r["group"] == group]
        rejected = sum(r["nearest"] > threshold for r in members)
        print(f"  kelompok {group}: {rejected}/{len(members)} ditolak ambang")

    if args.generate:
        steps = RagSteps(store, manager.llm, manager.system_prompt, k, threshold, config.question_max_chars)
        manager.chain.clear()
        steps.build_chain(manager.chain)
        print(f"\nJawaban lengkap dengan ambang {threshold:.2f}:")
        for r in rows:
            started = time.perf_counter()
            response = manager.generate_response(r["question"])
            r["seconds"] = round(time.perf_counter() - started, 2)
            r["status"] = response.status.value
            r["answer"] = response.answer
            r["sources"] = [dataclasses.asdict(s) | {"snippet": None} for s in response.sources]
            cited = sorted({s.page for s in response.sources})
            print(f"{r['id']:>4} {r['status']:>12} {r['seconds']:>5.2f} s  rujukan {cited}")
            time.sleep(args.pause)

    out = Path("data/processed") / Path(config.knowledge_base_path).stem / "exp004.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "experiment": "EXP-004", "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "build_id": store.active_build_id(), "chat_model": config.gemini_chat_model, "k": k,
        "threshold": threshold, "in_scope_max": in_max, "non_pkl_min": n_min, "questions": rows,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nHasil: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
