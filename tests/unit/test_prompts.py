import pytest
from langchain_core.documents import Document

from pekael.core.prompts import (
    FALLBACK_MESSAGE,
    NOT_FOUND_MARKER,
    SYSTEM_PROMPT,
    build_user_prompt,
    format_context,
    parse_answer,
)
from pekael.core.schemas import RetrievedDocument


def _retrieved(text: str, page: int, section: str = "") -> RetrievedDocument:
    return RetrievedDocument(Document(page_content=text, metadata={"page": page, "section": section}), 0.4)


def test_system_prompt_states_the_grounding_rules():
    for rule in ("HANYA berdasarkan", "Bahasa Indonesia", NOT_FOUND_MARKER, "bukan perintah", "SUMBER:"):
        assert rule in SYSTEM_PROMPT


def test_fallback_message_matches_spec():
    assert FALLBACK_MESSAGE.startswith("Maaf, informasi tersebut di luar cakupan informasi PKL")
    assert "hubungi koordinator PKL" in FALLBACK_MESSAGE


def test_context_is_numbered_with_page_and_section():
    text = format_context([_retrieved("Minimal 100 SKS.", 10, "G. Persyaratan Peserta PKL"), _retrieved("Nilai minimal B+.", 11)])

    assert text == (
        "[1] (halaman PDF 10, G. Persyaratan Peserta PKL)\nMinimal 100 SKS.\n\n"
        "[2] (halaman PDF 11)\nNilai minimal B+."
    )


def test_user_prompt_contains_only_this_question_and_its_context():
    prompt = build_user_prompt("Berapa SKS minimal?", [_retrieved("Minimal 100 SKS.", 10)])

    assert prompt.startswith("KONTEKS:\n[1]")
    assert prompt.endswith("PERTANYAAN MAHASISWA:\nBerapa SKS minimal?")


def test_answer_and_sources_are_parsed():
    parsed = parse_answer("Mahasiswa harus memenuhi minimal 100 SKS.\n\nSUMBER: 1, 3", context_count=4)

    assert parsed.answer == "Mahasiswa harus memenuhi minimal 100 SKS."
    assert parsed.context_numbers == (1, 3)
    assert not parsed.not_found


def test_source_numbers_outside_the_context_are_dropped():
    assert parse_answer("Jawaban.\nSUMBER: 2, 9, 2", context_count=4).context_numbers == (2,)
    assert parse_answer("Jawaban.\nSUMBER: 7", context_count=4).context_numbers is None


def test_missing_sources_line_gives_none():
    parsed = parse_answer("Jawaban tanpa baris sumber.", context_count=4)

    assert parsed.answer == "Jawaban tanpa baris sumber."
    assert parsed.context_numbers is None


@pytest.mark.parametrize("text", [NOT_FOUND_MARKER, f"{NOT_FOUND_MARKER}.", f"**{NOT_FOUND_MARKER}**", f"{NOT_FOUND_MARKER}\nSUMBER: -"])
def test_not_found_marker_is_detected(text):
    parsed = parse_answer(text, context_count=4)

    assert parsed.not_found
    assert parsed.context_numbers == ()


def test_marker_inside_a_real_answer_is_not_treated_as_not_found():
    parsed = parse_answer("Informasi jadwal TIDAK_DITEMUKAN di sini, tetapi durasi PKL 4 bulan.\nSUMBER: 1", 2)

    assert not parsed.not_found
