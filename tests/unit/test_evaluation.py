import json
import subprocess
import sys

import pytest

from pekael.evaluation.dataset import SPRINT4_IDS, load_dataset, select
from pekael.evaluation.ragas_evaluator import explain_answer_relevancy, explain_context_recall, explain_faithfulness


def _write(tmp_path, rows):
    path = tmp_path / "gt.jsonl"
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    return path


def _row(id_, category="pkl"):
    return {"id": id_, "category": category, "user_input": f"Pertanyaan {id_}?", "reference": "Jawaban acuan.",
            "reference_contexts": ["konteks"], "reference_sources": [{"source_file": "a.pdf", "page": 1}], "version": "v2",
            "expected_status": "answered"}


def test_sprint4_scope_is_the_36_test_questions():
    assert len(SPRINT4_IDS) == 36 and SPRINT4_IDS[0] == "1" and SPRINT4_IDS[-1] == "E6"


def test_dataset_is_loaded_and_selected_by_scope(tmp_path):
    rows = [_row("1"), _row("E6"), _row("L4"), _row("L1", "pkl_redirect"), _row("N1", "non_pkl")]
    entries = load_dataset(_write(tmp_path, rows))

    assert [e.id for e in select(entries, "uji36")] == ["1", "E6"]
    assert [e.id for e in select(entries, "pkl")] == ["1", "E6", "L4"]
    assert len(select(entries, "all")) == 5
    assert [e.id for e in select(entries, ids=["L4"])] == ["L4"]
    assert entries[0].reference_contexts == ("konteks",)
    with pytest.raises(ValueError):
        select(entries, ids=["99"])


def test_duplicate_or_incomplete_rows_are_rejected(tmp_path):
    with pytest.raises(ValueError, match="Duplicate"):
        load_dataset(_write(tmp_path, [_row("1"), _row("1")]))
    broken = _row("2")
    broken["reference"] = ""
    with pytest.raises(ValueError, match="lacks"):
        load_dataset(_write(tmp_path, [broken]))


def test_faithfulness_explanation_counts_supported_statements():
    calls = [
        {"output_type": "StatementGeneratorOutput", "output": {"statements": ["A", "B"]}},
        {"output_type": "NLIStatementOutput", "output": {"statements": [
            {"statement": "A", "reason": "ada", "verdict": 1}, {"statement": "B", "reason": "tidak ada", "verdict": 0}]}},
    ]

    details = explain_faithfulness(calls)

    assert (details["supported"], details["total"]) == (1, 2)
    assert details["statements"] == ["A", "B"]


def test_answer_relevancy_explanation_gives_each_cosine_similarity():
    calls = [{"output_type": "AnswerRelevanceOutput", "output": {"question": "Q1", "noncommittal": 0}},
             {"output_type": "AnswerRelevanceOutput", "output": {"question": "Q2", "noncommittal": 1}}]
    vectors = [("Asli?", [1.0, 0.0]), ("Q1", [1.0, 0.0]), ("Q2", [0.0, 1.0])]

    details = explain_answer_relevancy("Asli?", calls, vectors)

    assert [q["cosine_similarity"] for q in details["generated_questions"]] == pytest.approx([1.0, 0.0])
    assert details["all_noncommittal"] is False


def test_context_recall_explanation_counts_attributed_statements():
    calls = [{"output_type": "ContextRecallOutput", "output": {"classifications": [
        {"statement": "A", "reason": "r", "attributed": 1}, {"statement": "B", "reason": "r", "attributed": 1},
        {"statement": "C", "reason": "r", "attributed": 0}]}}]

    assert explain_context_recall(calls)["attributed"] == 2


def test_chatbot_does_not_import_ragas_or_the_evaluator_clients():
    code = ("import sys, pekael.ui.student_page, pekael.evaluation.dataset;"
            "print([m for m in ('ragas', 'openai', 'pekael.evaluation.ragas_evaluator') if m in sys.modules])")
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True).stdout.strip()

    assert out == "[]"  # FR-11: Ragas and its clients load only in the evaluation script
