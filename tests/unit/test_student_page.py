from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from pekael.config.settings import AppConfig, ConfigError
from pekael.core.prompts import FALLBACK_MESSAGE
from pekael.core.schemas import ChatbotResponse, ResponseStatus, SourceReference
from pekael.ui import student_page
from pekael.vectorstores.base import IndexNotReadyError

APP = str(Path(__file__).resolve().parents[2] / "app.py")
SOURCES = (
    SourceReference("Pedoman-PKL-2025.pdf", 10, "c1", "G. Persyaratan Peserta PKL", "Mahasiswa dapat menjadi peserta PKL jika telah memenuhi minimal 100 SKS."),
    SourceReference("Pedoman-PKL-2025.pdf", 10, "c2", None, "Kutipan kedua."),
    SourceReference("Pedoman-PKL-2025.pdf", 13, "c3", "A. Prosedur", "Kutipan ketiga."),
)


class FakeStore:
    def __init__(self, ready: bool = True) -> None:
        self.ready = ready
        self.is_ready = False

    def load(self):
        if not self.ready:
            raise IndexNotReadyError("Knowledge base has not been built yet")
        self.is_ready = True


class FakeManager:
    def __init__(self, response: ChatbotResponse | None = None, ready: bool = True) -> None:
        self.vector_store = FakeStore(ready)
        self.response = response or ChatbotResponse("Minimal 100 SKS.", ResponseStatus.ANSWERED, SOURCES)
        self.questions: list[str] = []

    def generate_response(self, message):
        self.questions.append(message)
        return self.response


@pytest.fixture
def app(monkeypatch):
    def start(manager=None, error: Exception | None = None):
        def get_manager():
            if error:
                raise error
            return manager

        monkeypatch.setattr(student_page, "get_manager", get_manager)
        monkeypatch.setattr(student_page, "get_config", lambda: AppConfig(question_max_chars=500))
        return AppTest.from_file(APP, default_timeout=30).run()

    return start


def _ask(at: AppTest, question: str) -> AppTest:
    at.text_area[0].input(question)
    return at.button[0].click().run()


def test_first_view_shows_title_question_box_and_note(app):
    at = app(FakeManager())

    assert at.title[0].value == "Pekael"
    assert at.text_area[0].label == "Pertanyaan tentang PKL"
    assert at.text_area[0].max_chars == 500
    assert at.button[0].label == "Kirim"
    assert not at.warning
    assert "koordinator PKL" in at.caption[-1].value


def test_answer_shows_document_pages_and_quotes(app):
    manager = FakeManager()

    at = _ask(app(manager), "Berapa SKS minimal?")

    assert manager.questions == ["Berapa SKS minimal?"]
    assert "Minimal 100 SKS." in [m.value for m in at.markdown]
    assert any(c.value == "Sumber: Pedoman PKL 2025, halaman PDF 10, 13" for c in at.caption)
    assert at.expander[0].label == "Lihat kutipan dari buku pedoman"
    assert any("Halaman PDF 10 · G. Persyaratan Peserta PKL" in m.value for m in at.markdown)


def test_out_of_scope_answer_is_shown_without_sources(app):
    at = _ask(app(FakeManager(ChatbotResponse(FALLBACK_MESSAGE, ResponseStatus.OUT_OF_SCOPE))), "Apa itu machine learning?")

    assert at.info[0].value == FALLBACK_MESSAGE
    assert not at.expander


def test_service_problem_is_shown_as_warning(app):
    response = ChatbotResponse("Kuota layanan AI Pekael sedang habis.", ResponseStatus.UNAVAILABLE)

    at = _ask(app(FakeManager(response)), "Berapa SKS minimal?")

    assert at.warning[0].value == response.answer


def test_empty_question_warns_and_is_not_kept(app):
    response = ChatbotResponse("Silakan tulis pertanyaan tentang PKL terlebih dahulu.", ResponseStatus.INVALID_INPUT)

    at = _ask(app(FakeManager(response)), "")

    assert at.warning[0].value == response.answer
    assert at.session_state[student_page.HISTORY_KEY] == []


def test_newest_question_is_shown_first_and_history_can_be_cleared(app):
    at = _ask(app(FakeManager()), "Pertanyaan pertama")
    at = _ask(at, "Pertanyaan kedua")

    questions = [m.value for m in at.markdown if m.value.startswith("**Pertanyaan")]
    assert questions == ["**Pertanyaan kedua**", "**Pertanyaan pertama**"]

    at = at.button[1].click().run()  # "Hapus riwayat"
    assert at.session_state[student_page.HISTORY_KEY] == []


def test_missing_knowledge_base_disables_the_form(app):
    at = app(FakeManager(ready=False))

    assert at.warning[0].value == student_page.NOT_READY
    assert at.text_area[0].disabled
    assert at.button[0].disabled


def test_missing_settings_disable_the_form_without_details(app):
    at = app(error=ConfigError("Missing required settings: GEMINI_API_KEY"))

    assert at.warning[0].value == student_page.NOT_CONFIGURED
    assert "GEMINI_API_KEY" not in at.warning[0].value
    assert at.button[0].disabled


def test_document_name_is_readable():
    assert student_page.document_name("Pedoman-PKL-2025.pdf") == "Pedoman PKL 2025"
