import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "export_docs.py"
spec = importlib.util.spec_from_file_location("export_docs", SCRIPT)
export_docs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(export_docs)

SCRUM = export_docs.SCRUM_DIR


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        (SCRUM / "sprint-01" / "sprint_planning.md", ("SPRINT REPORT 1", "Bagian A: Sprint Planning", "Sprint Report 1: Sprint Planning")),
        (SCRUM / "sprint-03" / "validasi_review.md", ("LEMBAR VALIDASI SPRINT REPORT 3", "Bagian C: Sprint Review", "Lembar Validasi Sprint Report 3: Sprint Review")),
        (SCRUM / "product_backlog.md", export_docs.OTHER_DOCUMENTS["product_backlog"]),
    ],
)
def test_header_titles_per_document(path, expected):
    assert export_docs.document_titles(path) == expected


@pytest.mark.parametrize("path", [SCRUM / "README.md", SCRUM / "templates" / "sprint_planning.md", SCRUM / "sprint-01" / "notes.md"])
def test_unknown_documents_are_skipped(path):
    assert export_docs.document_titles(path) is None


def _table(text: str, header: bool) -> str:
    row_header = "<w:trPr><w:tblHeader/></w:trPr>" if header else ""
    return f'<w:tbl><w:tblPr><w:tblW w:type="auto" w:w="0"/></w:tblPr><w:tr>{row_header}<w:tc><w:p><w:r><w:t>{text}</w:t></w:r></w:p></w:tc></w:tr></w:tbl>'


def test_tables_fill_the_text_width():
    result = export_docs._format_tables(_table("ID", header=True))

    assert '<w:tblW w:type="pct" w:w="5000"/>' in result
    assert "w:val=\"nil\"" not in result


@pytest.mark.parametrize(
    "table",
    [_table("Periode", header=False), _table("Product Owner Developer NIM", header=True)],
)
def test_label_value_and_signature_tables_have_no_borders(table):
    assert '<w:top w:val="nil"/>' in export_docs._format_tables(table)


def test_personal_values_default_to_blank(monkeypatch, tmp_path):
    monkeypatch.setattr(export_docs, "ROOT", tmp_path)
    for name in export_docs.PERSONAL_PLACEHOLDERS:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("NIM_DEVELOPER", "123")

    values = export_docs._personal_values()

    assert values == {"NIM_DEVELOPER": "123", "NIP_PRODUCT_OWNER": export_docs.BLANK}
