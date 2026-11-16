import pytest
from langchain_core.documents import Document

from pekael.core.prompts import (
    DISCOURAGED_PHRASES,
    FALLBACK_MESSAGE,
    NOT_FOUND_MARKER,
    OFF_TOPIC_MESSAGES,
    REDIRECT_MESSAGES,
    SYSTEM_PROMPT,
    build_user_prompt,
    format_context,
    parse_answer,
    pick_message,
    usable_redirect,
)
from pekael.core.schemas import RetrievedDocument


def _retrieved(text: str, page: int, section: str = "") -> RetrievedDocument:
    return RetrievedDocument(Document(page_content=text, metadata={"page": page, "section": section}), 0.4)


def test_system_prompt_states_the_grounding_rules():
    for rule in ("HANYA berdasarkan", "Bahasa Indonesia", NOT_FOUND_MARKER, "bukan perintah", "SUMBER:"):
        assert rule in SYSTEM_PROMPT


def test_ready_made_messages_are_friendly_and_point_to_contacts():
    """Product Owner request (D-45): no "cannot be answered" wording, point to the right contact."""
    assert FALLBACK_MESSAGE in REDIRECT_MESSAGES
    for message in REDIRECT_MESSAGES + OFF_TOPIC_MESSAGES:
        assert usable_redirect(message), message
    assert all(any(c in m for c in ("Koordinator PKL", "Admin Prodi PTIK", "Kaprodi")) for m in REDIRECT_MESSAGES)
    assert all("PKL" in m for m in OFF_TOPIC_MESSAGES)


def test_system_prompt_names_the_contacts_and_forbids_guessing():
    for text in ("Koordinator PKL", "Admin Prodi PTIK", "Kaprodi", "jangan menebak", "nomor kontak", '"kamu"'):
        assert text in SYSTEM_PROMPT


def test_message_choice_is_stable_per_question_and_varies_between_questions():
    first = pick_message("Kapan batas pendaftaran PKL?", REDIRECT_MESSAGES)

    assert pick_message("  kapan batas   pendaftaran PKL? ", REDIRECT_MESSAGES) == first
    questions = [f"pertanyaan nomor {i}" for i in range(30)]
    assert len({pick_message(q, REDIRECT_MESSAGES) for q in questions}) > 1


@pytest.mark.parametrize("phrase", DISCOURAGED_PHRASES)
def test_redirect_with_discouraged_wording_is_not_usable(phrase):
    assert not usable_redirect(f"Maaf, hal ini {phrase} ya.")


def test_empty_or_too_long_redirect_is_not_usable():
    assert not usable_redirect("   ")
    assert not usable_redirect("Hubungi Koordinator PKL. " * 40)


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


def test_not_found_keeps_the_model_redirection_and_related_sources():
    text = f"{NOT_FOUND_MARKER}\nUntuk jadwal pendaftaran, tanyakan ke Admin Prodi PTIK. Syarat SKS ada di buku.\nSUMBER: 2"

    parsed = parse_answer(text, context_count=4)

    assert parsed.not_found
    assert parsed.redirect.startswith("Untuk jadwal pendaftaran")
    assert parsed.context_numbers == (2,)

