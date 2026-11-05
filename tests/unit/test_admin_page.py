from pathlib import Path

import pytest
from pydantic import SecretStr
from streamlit.proto.TextInput_pb2 import TextInput
from streamlit.testing.v1 import AppTest

from pekael.config.settings import AppConfig
from pekael.core.schemas import ChatbotResponse, IndexingReport, IngestionReport, ResponseStatus, SourceReference
from pekael.loaders.pdf_loader import DocumentLoadError
from pekael.ui import admin_page, student_page
from pekael.vectorstores.base import VectorStoreError

APP = str(Path(__file__).resolve().parents[1] / "fixtures" / "admin_app.py")
PASSWORD = "kata-sandi-uji"  # test-only value


class FakeStore:
    def __init__(self, source_path: str) -> None:
        self.is_ready = True
        self.activated = []
        self.manifest = {
            "build_id": "20261104T043244948591-565a9929",
            "created_at": "2026-11-04T04:32:44+00:00",
            "sources": [{"source_file": "Pedoman-PKL-2025.pdf", "source_hash": "565a9929ea00a999"}],
            "pages": [4, 5, 6],
            "chunk_count": 5,
            "dimension": 768,
            "source_path": source_path,
        }

    def load(self):
        pass

    def versions(self):
        old = {**self.manifest, "build_id": "20261102T180419398924-565a9929", "created_at": "2026-11-02T18:04:19+00:00"}
        return [{**self.manifest, "active": True}, {**old, "active": False}]

    def activate_version(self, build_id):
        self.activated.append(build_id)

    def total_pages(self):
        return 8

    def chunks_per_page(self):
        return {4: 1, 5: 3, 6: 1}


class FakeManager:
    def __init__(self, source_path: str, error: Exception | None = None) -> None:
        self.vector_store = FakeStore(source_path)
        self.error = error
        self.builds = []
        self.cleared = 0

    def cached_answers(self):
        return 3

    def clear_cache(self):
        self.cleared += 1

    def initialize_knowledge_base(self, source, pages=None, on_progress=None):
        self.builds.append((Path(source).name, pages))
        for stage, done, total in (("load", 0, 0), ("load", 1, 3), ("load", 3, 3), ("split", 0, 0), ("index", 0, 5)):
            on_progress(stage, done, total)
        if self.error:
            raise self.error
        indexing = IndexingReport("20261105T000000000000-565a9929", 5, "gemini-embedding-001", 768, "data/index/versions/x")
        return IngestionReport("Pedoman-PKL-2025.pdf", "565a9929", 3, 0, 3, 5, indexing,
                               ("OCR pages without a correction file, confirm they were checked: [5]",))

    def generate_response(self, message, on_step=None):
        source = SourceReference("Pedoman-PKL-2025.pdf", 10, "c1", None, "Kutipan")
        return ChatbotResponse("Minimal 100 SKS.", ResponseStatus.ANSWERED, (source,), (0.42, 0.51))


class FakeOcr:
    def __init__(self, *args) -> None:
        pass

    def check_available(self):
        return "5.4.0"


@pytest.fixture
def admin(monkeypatch, tmp_path):
    source = tmp_path / "Pedoman-PKL-2025.pdf"
    source.write_bytes(b"%PDF-1.7 test")

    def start(manager=None, configured: bool = True, signed_in: bool = False):
        manager = manager or FakeManager(str(source))
        config = AppConfig(
            admin_username="admin1" if configured else None,
            admin_password=SecretStr(PASSWORD) if configured else None,
            knowledge_base_pages="4-6",
            retrieval_max_l2_distance=0.64,
        )
        monkeypatch.setattr(student_page, "get_config", lambda: config)
        monkeypatch.setattr(student_page, "get_manager", lambda: manager)
        monkeypatch.setattr(admin_page, "OcrService", FakeOcr)
        at = AppTest.from_file(APP, default_timeout=30)
        if signed_in:
            at.session_state[admin_page.AUTH_KEY] = "admin1"
        at = at.run()
        at.manager = manager
        return at

    return start


def _html(at) -> str:
    return "\n".join(m.value for m in at.markdown)


def _login(at, username="admin1", password=PASSWORD):
    at.text_input[0].input(username)
    at.text_input[1].input(password)
    return at.button[0].click().run()


def test_login_card_is_shown_first(admin):
    at = admin()

    assert "ruang admin" in _html(at) and "RUANG ADMIN" in _html(at)
    assert [t.label for t in at.text_input] == ["Nama pengguna", "Kata sandi"]
    assert at.text_input[1].proto.type == TextInput.PASSWORD
    assert not at.tabs


def test_wrong_password_is_rejected(admin):
    at = _login(admin(), password="salah")

    assert at.error[0].value == "Nama pengguna atau kata sandi salah."
    assert admin_page.AUTH_KEY not in at.session_state


def test_correct_login_opens_dashboard(admin):
    at = _login(admin())

    html = _html(at)
    assert at.session_state[admin_page.AUTH_KEY] == "admin1"
    assert "Halo, <span class=\"pk-soft\">admin1</span>." in html
    assert "Pedoman PKL 2025" in html and "4–6" in html
    assert html.count('class="pk-tile') == 8
    assert 'title="Halaman 5: 3 potongan"' in html
    assert [t.label for t in at.tabs] == ["Ganti buku pedoman", "Riwayat versi", "Uji pertanyaan", "Pengaturan"]


def test_empty_fields_ask_to_type_and_do_not_count_as_failure(admin):
    at = _login(admin(), username="", password="")

    assert "Isi nama pengguna dan kata sandi" in at.warning[0].value
    assert not at.error
    assert admin_page.FAILS_KEY not in at.session_state  # not counted as a failed attempt


def test_autofill_is_turned_off(admin):
    at = admin()

    assert [t.proto.autocomplete for t in at.text_input] == ["off", "new-password"]


def test_five_failures_lock_the_form(admin):
    at = admin()
    for _ in range(admin_page.MAX_FAILS):
        at = _login(at, password="salah")
    at = at.run()

    assert at.button[0].disabled
    assert "Terlalu banyak percobaan" in at.warning[0].value


def test_login_disabled_without_configured_account(admin):
    at = admin(configured=False)

    assert "Login admin nonaktif" in at.warning[0].value
    assert not at.text_input


def test_logout_returns_to_login(admin):
    at = admin(signed_in=True)

    at = at.button(key="pk-logout").click().run()

    assert admin_page.AUTH_KEY not in at.session_state
    assert len(at.text_input) == 2


def test_new_file_build_needs_upload_and_approval(admin):
    at = admin(signed_in=True)

    assert at.button(key="pk-build-new").disabled
    assert not at.button(key="pk-rebuild").disabled


def test_rebuild_current_book_reports_result(admin):
    at = admin(signed_in=True)

    at = at.button(key="pk-rebuild").click().run()

    assert at.manager.builds == [("Pedoman-PKL-2025.pdf", [4, 5, 6])]
    html = _html(at)
    assert "Knowledge base baru aktif" in html
    assert "halaman OCR [5] belum punya file koreksi" in html


def test_failed_build_keeps_old_knowledge_base(admin, tmp_path):
    source = tmp_path / "Pedoman-PKL-2025.pdf"
    at = admin(manager=FakeManager(str(source), error=VectorStoreError("Building the index failed: EmbeddingError")), signed_in=True)

    at = at.button(key="pk-rebuild").click().run()

    html = _html(at)
    assert "Pembangunan gagal." in html and "Knowledge base lama tetap dipakai" in html
    assert admin_page.REPORT_KEY not in at.session_state


def test_invalid_page_range_disables_building(admin):
    at = admin(signed_in=True)

    pages_box = next(t for t in at.text_input if t.label == "Halaman yang dipakai")
    at = pages_box.input("4-").run()

    assert at.button(key="pk-rebuild").disabled
    assert "Format halaman tidak valid" in at.warning[0].value


def test_old_version_can_be_activated(admin):
    at = admin(signed_in=True)

    at = at.button(key="pk-activate-20261102T180419398924-565a9929").click().run()

    assert at.manager.vector_store.activated == ["20261102T180419398924-565a9929"]
    assert at.manager.cleared == 1
    assert "aktif" in _html(at)


def test_try_question_shows_distances(admin):
    at = admin(signed_in=True)

    try_box = next(t for t in at.text_input if t.label == "Pertanyaan uji")
    try_box.input("Berapa SKS minimal?")
    at = next(b for b in at.button if b.label == "Coba").click().run()

    html = _html(at)
    assert "0.420, 0.510 (batas 0.64)" in html
    assert "Minimal 100 SKS." in html


def test_settings_show_values_without_secrets(admin):
    at = admin(signed_in=True)

    html = _html(at)
    assert "gemini-3.5-flash-lite" in html and "3 pertanyaan" in html
    assert PASSWORD not in html

    at = at.button(key="pk-clear-cache").click().run()
    assert at.manager.cleared == 1


def test_upload_must_be_a_pdf_within_size(tmp_path, monkeypatch):
    monkeypatch.setattr(admin_page, "UPLOAD_DIR", tmp_path)

    with pytest.raises(DocumentLoadError):
        admin_page.save_upload("a.pdf", b"bukan pdf", 30)
    with pytest.raises(DocumentLoadError):
        admin_page.save_upload("a.pdf", b"%PDF-" + b"0" * (1024 * 1024), 1)

    saved = admin_page.save_upload("../Buku Pedoman.pdf", b"%PDF-1.7", 30)
    assert saved.parent == tmp_path
    assert saved.name.endswith("-Buku-Pedoman.pdf")
