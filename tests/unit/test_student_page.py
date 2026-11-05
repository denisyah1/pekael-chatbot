from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from pekael.config.settings import AppConfig, ConfigError
from pekael.core.prompts import FALLBACK_MESSAGE
from pekael.core.schemas import ChatbotResponse, ResponseStatus, SourceReference
from pekael.ui import content, student_page, theme
from pekael.vectorstores.base import IndexNotReadyError

APP = str(Path(__file__).resolve().parents[2] / "app.py")
SOURCES = (
    SourceReference("Pedoman-PKL-2025.pdf", 10, "c1", "G. Persyaratan Peserta PKL", "Mahasiswa dapat menjadi peserta PKL jika telah memenuhi minimal 100 SKS."),
    SourceReference("Pedoman-PKL-2025.pdf", 10, "c2", None, "Kutipan kedua."),
    SourceReference("Pedoman-PKL-2025.pdf", 13, "c3", "A. Prosedur", "Kutipan ketiga."),
)
MANIFEST = {
    "sources": [{"source_file": "Pedoman-PKL-2025.pdf", "source_hash": "abc"}],
    "pages": [4, 5, 6, 7, 9],
    "chunk_count": 7,
    "created_at": "2026-11-04T04:32:44+00:00",
}


class FakeStore:
    def __init__(self, ready: bool = True) -> None:
        self.ready = ready
        self.is_ready = False
        self.manifest = None

    def load(self):
        if not self.ready:
            raise IndexNotReadyError("Knowledge base has not been built yet")
        self.is_ready, self.manifest = True, MANIFEST


class FakeManager:
    def __init__(self, response: ChatbotResponse | None = None, ready: bool = True) -> None:
        self.vector_store = FakeStore(ready)
        self.response = response or ChatbotResponse("Minimal 100 SKS.", ResponseStatus.ANSWERED, SOURCES)
        self.questions: list[str] = []
        self.reported: list[str] = []

    def generate_response(self, message, on_step=None):
        self.questions.append(message)
        for step in ("validate_input", "retrieve", "generate"):
            if on_step:
                on_step(step)
                self.reported.append(step)
        return self.response


@pytest.fixture
def app(monkeypatch):
    def start(manager=None, error: Exception | None = None, intro_done: bool = True):
        def get_manager():
            if error:
                raise error
            return manager

        monkeypatch.setattr(student_page, "get_manager", get_manager)
        monkeypatch.setattr(student_page, "get_config", lambda: AppConfig(question_max_chars=500))
        at = AppTest.from_file(APP, default_timeout=30)
        at.session_state[student_page.INTRO_KEY] = intro_done
        return at.run()

    return start


def _ask(at: AppTest, question: str) -> AppTest:
    return at.chat_input[0].set_value(question).run()


def _html(at: AppTest) -> str:
    return "\n".join(m.value for m in at.markdown)


def test_intro_shows_wordmark_and_start_button(app):
    at = app(FakeManager(), intro_done=False)

    assert 'aria-label="pekael"' in _html(at)
    assert "pe·ka·el" in _html(at)
    assert not at.chat_input

    at = at.button(key="pk-start").click().run()
    assert at.session_state[student_page.INTRO_KEY] is True
    assert len(at.chat_input) == 1


def test_welcome_shows_examples_facts_and_source(app):
    at = app(FakeManager())

    html = _html(at)
    assert content.GREETING.split(",")[0] in html
    assert [at.button(key=f"pk-ex-{i}").label for i in range(4)] == list(content.EXAMPLES)
    assert "100 SKS" in html and "hal. 10" in html
    assert "Pedoman PKL 2025 · 5 halaman" in html
    assert "Halaman PDF 4–7, 9" in html
    assert at.chat_input[0].max_chars == 500
    assert not at.warning


def test_answer_shows_bubble_page_tabs_quotes_and_progress(app):
    manager = FakeManager()

    at = _ask(app(manager), "Berapa SKS minimal?")

    html = _html(at)
    assert manager.questions == ["Berapa SKS minimal?"]
    assert manager.reported == ["validate_input", "retrieve", "generate"]
    assert '<div class="pk-q"><div>Berapa SKS minimal?</div><span class="pk-time">' in html  # question on the right, with time
    assert "Minimal 100 SKS." in html
    assert '<span class="pk-page">hal. 10</span><span class="pk-page">hal. 13</span>' in html
    assert at.expander[0].label == "Lihat kutipan dari buku pedoman"
    assert "Halaman PDF 10 · G. Persyaratan Peserta PKL" in html
    assert content.GREETING.split(",")[0] not in html  # welcome hidden after the first question


def test_example_button_asks_that_question(app):
    manager = FakeManager()

    app(manager).button(key="pk-ex-2").click().run()

    assert manager.questions == [content.EXAMPLES[2]]


def test_question_text_is_escaped(app):
    at = _ask(app(FakeManager()), "<b>tebal</b>")

    assert "&lt;b&gt;tebal&lt;/b&gt;" in _html(at)


def test_out_of_scope_and_service_problem_are_labelled(app):
    at = _ask(app(FakeManager(ChatbotResponse(FALLBACK_MESSAGE, ResponseStatus.OUT_OF_SCOPE))), "Apa itu machine learning?")
    assert "Tidak ada di buku pedoman" in _html(at)
    assert not at.expander

    at = _ask(app(FakeManager(ChatbotResponse("Pekael sedang sibuk.", ResponseStatus.UNAVAILABLE))), "Berapa SKS?")
    assert "Perlu dicoba lagi" in _html(at) and "pk-warn" in _html(at)


def test_empty_question_is_not_kept(app):
    response = ChatbotResponse("Silakan tulis pertanyaan tentang PKL terlebih dahulu.", ResponseStatus.INVALID_INPUT)

    at = _ask(app(FakeManager(response)), "   ")

    assert at.session_state[student_page.HISTORY_KEY] == []
    assert at.toast[0].value == response.answer


def test_questions_stay_in_order_and_new_conversation_clears(app):
    at = _ask(app(FakeManager()), "Pertanyaan pertama")
    at = _ask(at, "Pertanyaan kedua")

    html = _html(at)
    assert html.index("Pertanyaan pertama") < html.index("Pertanyaan kedua")

    at = at.button(key="pk-clear").click().run()
    assert at.session_state[student_page.HISTORY_KEY] == []


def test_missing_knowledge_base_disables_input(app):
    at = app(FakeManager(ready=False))

    assert at.warning[0].value == content.NOT_READY
    assert at.chat_input[0].disabled
    assert at.button(key="pk-ex-0").disabled


def test_missing_settings_disable_input_without_details(app):
    at = app(error=ConfigError("Missing required settings: GEMINI_API_KEY"))

    assert at.warning[0].value == content.NOT_CONFIGURED
    assert "GEMINI_API_KEY" not in _html(at)
    assert at.chat_input[0].disabled


def test_formatting_helpers():
    assert student_page.document_name("Pedoman-PKL-2025.pdf") == "Pedoman PKL 2025"
    assert student_page.page_ranges([4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 22, 23, 24, 25, 27, 28]) == "4–16, 22–25, 27–28"
    assert student_page.readable_date("2026-11-04T04:32:44+00:00") == "4 November 2026"
    assert theme.loading("Membuka buku pedoman", 1, 3).count("<u") == 3


def test_facts_quote_verified_pages():
    assert {(f.figure, f.page) for f in content.FACTS} == {
        ("100 SKS", 10), ("4 bulan", 14), ("B+", 11), ("6 SKS", 13), ("30 · 40 · 30", 28), ("8 dokumen", 24)
    }
    assert set(content.STEP_LABELS) == {
        "validate_input", "retrieve", "relevancy_gate", "build_prompt", "generate", "validate_citations"
    }
