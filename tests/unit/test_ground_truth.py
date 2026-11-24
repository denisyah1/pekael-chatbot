import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


build_ground_truth = _load("build_ground_truth")


def test_dataset_holds_the_44_questions_tested_since_sprint_3():
    gt = build_ground_truth
    sprint4 = (ROOT / "docs/scrum/sprint-04/pertanyaan_uji.md").read_text(encoding="utf-8")
    in_scope = dict(re.findall(r"^\| (\w+) \| [^|]+ \| ([^|]+?) \|", sprint4, re.MULTILINE))
    sys.path.insert(0, str(ROOT / "scripts"))
    experiment = _load("run_chunk_experiment")
    _, outside = experiment.load_questions(experiment.TOPICS)
    outside = {q["id"]: q["question"] for q in outside}

    ids = [e[0] for e in gt.ANSWERED] + [e[0] for e in gt.REDIRECTED] + [e[0] for e in gt.NON_PKL]
    assert len(ids) == len(set(ids)) == gt.TOTAL == 44
    for id_, _, _, question, *_ in gt.PKL:
        assert in_scope[id_] == question  # same wording as the Sprint 4 test questions
    for id_, _, _, question, *_ in gt.ANSWERED_BY_EXTRA:
        assert outside[id_] == question
    for id_, _, question, _ in gt.REDIRECTED + gt.NON_PKL:
        assert outside[id_] == question
    assert set(outside) == {e[0] for e in gt.ANSWERED_BY_EXTRA + gt.REDIRECTED + gt.NON_PKL}


def test_every_answered_entry_has_sources_and_the_sheet_shows_no_pages():
    gt = build_ground_truth
    assert all(entry[5] for entry in gt.ANSWERED)
    sheet = gt.sheet()

    assert not re.search(r"halaman (pdf|sumber|\d)|hal\. \d|hlm\.", sheet, re.IGNORECASE)  # no source pages
    assert ";" not in sheet
    assert sheet.count("☐ Sesuai") == 44
