import pytest
from langchain_core.documents import Document

from pekael.core.prompts import (
    CONVERSATION_PROMPT,
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
    usable_conversation,
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
    for text in ("Koordinator PKL", "Admin Prodi PTIK", "Kaprodi", "jangan menebak", "nomor kontak"):
        assert text in SYSTEM_PROMPT


def test_prompts_ask_to_match_the_students_register_and_paraphrase():
    for prompt in (SYSTEM_PROMPT, CONVERSATION_PROMPT):
        assert 'sapaan "kamu"' in prompt and 'sapaan "Anda"' in prompt
        assert "kalimatmu sendiri" in prompt
    assert "Jangan memberi informasi PKL apa pun" in CONVERSATION_PROMPT
    assert "Pertanyaan berupa kasus" in SYSTEM_PROMPT and "Hanya jika tidak ada satu pun informasi" in SYSTEM_PROMPT
    assert "jangan memanggil mahasiswa" in SYSTEM_PROMPT
    assert "SKS-mu" not in SYSTEM_PROMPT  # no example sentences the model could copy
    assert "{" not in SYSTEM_PROMPT and "{" not in CONVERSATION_PROMPT  # no unfilled placeholder


def test_conversational_reply_must_not_state_numbers():
    assert usable_conversation("Halo juga, semangat ya! Ada yang mau ditanyakan soal PKL?")
    assert not usable_conversation("PKL itu minimal 4 bulan.")


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


@pytest.mark.parametrize(
    "text",
    [NOT_FOUND_MARKER, f"{NOT_FOUND_MARKER}.", f"**{NOT_FOUND_MARKER}**", f"{NOT_FOUND_MARKER}\nSUMBER: -",
     "TIDAK_DITEMUCHAP\nTanyakan ke Admin Prodi PTIK ya.", "Tidak ditemukan", "TIDAK_DITEMUCH tanya admin ya"],
)
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


@pytest.mark.parametrize(
    ("question", "register"),
    [
        ("kak PKL tuh brp lama sih?", "santai"),
        ("kalo nilai aku 74 lulus gak?", "santai"),
        ("Mohon informasi mengenai durasi pelaksanaan PKL.", "formal"),
        ("Bagaimana prosedur pengajuan PKL bagi mahasiswa PTIK?", "formal"),
        ("Berapa SKS minimal untuk PKL?", "netral"),
    ],
)
def test_register_is_detected_from_the_wording(question, register):
    from pekael.core.prompts import detect_register

    assert detect_register(question) == register


def test_opening_greeting_is_dropped_unless_the_student_greets():
    from pekael.core.prompts import strip_unasked_greeting

    assert strip_unasked_greeting("Berapa lama PKL?", "Halo! PKL minimal 4 bulan.") == "PKL minimal 4 bulan."
    assert strip_unasked_greeting("halo kak, berapa lama PKL?", "Halo! PKL minimal 4 bulan.") == "Halo! PKL minimal 4 bulan."
    assert strip_unasked_greeting("Berapa lama PKL?", "Halaman 7 menyebut 4 bulan.") == "Halaman 7 menyebut 4 bulan."


def test_every_prompt_carries_one_presentation_form_picked_at_random():
    import random as _random

    from pekael.core.prompts import ANSWER_FORMS, CONVERSATION_FORMS, REDIRECT_FORMS, build_conversation_prompt

    prompt = build_user_prompt("Berapa SKS minimal?", [_retrieved("Minimal 100 SKS.", 10)], rng=_random.Random(1))
    answer_form = next(f for f in ANSWER_FORMS if f in prompt)
    assert not any(f in prompt for f in REDIRECT_FORMS)  # a redirection hint next to the question caused redirects
    assert "Isi daftar tetap lengkap" in prompt
    forms = {next(f for f in ANSWER_FORMS if f in build_user_prompt("x", [], rng=_random.Random(seed))) for seed in range(40)}
    assert len(forms) > 2 and answer_form in forms
    assert any(f in build_conversation_prompt("halo kak", rng=_random.Random(2)) for f in CONVERSATION_FORMS)


def test_ready_made_messages_have_more_variants():
    assert len(REDIRECT_MESSAGES) >= 6 and len(OFF_TOPIC_MESSAGES) >= 6


@pytest.mark.parametrize(
    "text",
    ["TIDAK_DITEMUCH TAPI TANYA ADMIN PRODI PTIK YAA", "TIDAK_DITEMUKAN Tanyakan ke Admin Prodi PTIK ya.", "**TIDAK DITEMUKAN**\nTanya Koordinator PKL"],
)
def test_marker_followed_by_text_on_the_same_line_is_detected(text):
    parsed = parse_answer(text, context_count=4)

    assert parsed.not_found
    assert "TIDAK" not in parsed.redirect.upper().split(" ")[0]


def test_answer_starting_with_the_word_tidak_is_not_a_marker():
    parsed = parse_answer("Tidak, nilai 74 belum memenuhi syarat B+.\nSUMBER: 1", context_count=2)

    assert not parsed.not_found


def test_shouting_redirect_is_not_usable():
    assert not usable_redirect("TAPI TANYA ADMIN PRODI PTIK YAA, BIAR NANTI DIBANTU CEK LAGI.")


def test_redirect_form_is_a_closing_note_of_the_system_prompt():
    import random as _random

    from pekael.core.prompts import REDIRECT_FORMS, system_prompt_with_redirect_form

    prompt = system_prompt_with_redirect_form(SYSTEM_PROMPT, rng=_random.Random(3))

    assert prompt.startswith(SYSTEM_PROMPT)
    assert any(f in prompt for f in REDIRECT_FORMS)


def test_greeting_question_sentence_is_dropped_when_not_greeted():
    from pekael.core.prompts import strip_unasked_greeting

    answer = "Hai, kamu mau tahu tentang PKL ya? PKL adalah kegiatan kurikuler."

    assert strip_unasked_greeting("apa itu pkl?", answer) == "PKL adalah kegiatan kurikuler."

