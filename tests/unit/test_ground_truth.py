import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("build_ground_truth", ROOT / "scripts" / "build_ground_truth.py")
build_ground_truth = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_ground_truth)


def test_dataset_has_the_36_test_questions_and_4_outside_pkl():
    ids = [entry[0] for entry in build_ground_truth.PKL] + [entry[0] for entry in build_ground_truth.NON_PKL]
    sprint4 = (ROOT / "docs/scrum/sprint-04/pertanyaan_uji.md").read_text(encoding="utf-8")
    questions = dict(re.findall(r"^\| (\w+) \| [^|]+ \| ([^|]+?) \|", sprint4, re.MULTILINE))

    assert len(ids) == len(set(ids)) == 40
    for id_, _, _, question, *_ in build_ground_truth.PKL:
        assert questions[id_] == question  # same wording as the Sprint 4 test questions


def test_every_pkl_answer_has_sources_and_the_sheet_shows_no_pages():
    assert all(entry[5] for entry in build_ground_truth.PKL)
    sheet = build_ground_truth.sheet()

    assert not re.search(r"halaman (pdf|sumber|\d)|hal\. \d|hlm\.", sheet, re.IGNORECASE)  # no source pages
    assert ";" not in sheet
    assert sheet.count("☐ Sesuai") == 40
