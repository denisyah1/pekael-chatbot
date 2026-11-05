"""Admin room (spec §12 Sprint 4, FR-06, FR-07, FR-08).

One admin account read from configuration (ADMIN_USERNAME, ADMIN_PASSWORD), never from code.
The admin can replace or rebuild the handbook, switch back to a stored version, try a
question with its retrieval distances, and see the active settings. A failed build keeps
the knowledge base students are using.
"""

import logging
import time
from datetime import datetime
from html import escape
from pathlib import Path

import streamlit as st

from pekael.config.settings import AppConfig
from pekael.core.chatbot_manager import BUILD_STAGES, ChatbotManager
from pekael.core.schemas import IngestionReport, ResponseStatus
from pekael.loaders.pdf_loader import DocumentLoadError, parse_page_ranges
from pekael.models.embeddings import EmbeddingError
from pekael.services.admin_auth import AdminAuthenticator
from pekael.services.ocr_service import OcrService, OcrUnavailableError
from pekael.ui import student_page, theme
from pekael.vectorstores.base import IndexNotReadyError, VectorStoreError

logger = logging.getLogger(__name__)

AUTH_KEY = "admin_user"
FAILS_KEY = "admin_fails"
LOCK_KEY = "admin_locked_until"
REPORT_KEY = "admin_report"
MAX_FAILS = 5
LOCK_SECONDS = 30
UPLOAD_DIR = Path("data/source/uploads")
STAGE_TEXT = {
    "load": "Membaca halaman buku",
    "split": "Memotong teks per halaman",
    "index": "Membuat vektor dan menyimpan versi baru",
}
BUILD_ERRORS = {
    DocumentLoadError: "File tidak dapat dibaca sebagai PDF, atau halaman yang dipilih melebihi jumlah halaman buku.",
    OcrUnavailableError: "Tesseract OCR tidak ditemukan, padahal buku ini hasil scan.",
    EmbeddingError: "Layanan embedding Gemini menolak atau tidak dapat dihubungi.",
    VectorStoreError: "Penyimpanan knowledge base gagal.",
}


def indonesian_date(moment: datetime) -> str:
    return f"{moment.day} {student_page.MONTHS[moment.month - 1]} {moment.year}"


# ---------- login ----------

def render_login(config: AppConfig) -> None:
    st.markdown(theme.login_card(f"PKL-{datetime.now():%Y}-01"), unsafe_allow_html=True)
    if not config.admin_enabled:
        st.warning("Login admin nonaktif karena ADMIN_USERNAME dan ADMIN_PASSWORD belum diatur di pengaturan.", icon=":material/lock:")
        return
    locked_for = st.session_state.get(LOCK_KEY, 0) - time.time()
    with st.container(key="pk-login"), st.form("pk-login-form", border=False):
        # Browser autofill is turned off: autofilled values are sometimes shown but not sent to the server.
        username = st.text_input("Nama pengguna", autocomplete="off")
        password = st.text_input("Kata sandi", type="password", autocomplete="new-password")
        submitted = st.form_submit_button("Masuk", disabled=locked_for > 0)
    if locked_for > 0:
        st.warning(f"Terlalu banyak percobaan. Coba lagi dalam {int(locked_for) + 1} detik.", icon=":material/timer:")
    elif submitted and not (username.strip() and password.strip()):
        st.warning("Isi nama pengguna dan kata sandi. Bila sudah terisi otomatis oleh browser, ketik ulang secara manual.",
                   icon=":material/edit:")
    elif submitted:
        if AdminAuthenticator(config.admin_username, config.admin_password).verify(username, password):
            st.session_state[AUTH_KEY] = username.strip()
            st.session_state[FAILS_KEY] = 0
            logger.info("Admin signed in")
            st.rerun()
        fails = st.session_state.get(FAILS_KEY, 0) + 1
        st.session_state[FAILS_KEY] = fails
        user_ok = username.strip().casefold() == (config.admin_username or "").strip().casefold()
        logger.warning("Admin sign-in failed (%d), username %s", fails, "matches" if user_ok else "does not match")
        if fails >= MAX_FAILS:
            st.session_state[LOCK_KEY] = time.time() + LOCK_SECONDS
            st.session_state[FAILS_KEY] = 0
        st.error("Nama pengguna atau kata sandi salah.", icon=":material/key_off:")
    st.markdown('<div class="pk-back"><a href="./" target="_self">← Kembali ke Pekael</a></div>', unsafe_allow_html=True)


# ---------- building ----------

def run_build(manager: ChatbotManager, source: Path, pages: list[int] | None) -> IngestionReport | None:
    """Build a new knowledge base version with a progress view. Returns None when it failed."""
    box = st.empty()
    bar = st.progress(0.0)

    def progress(stage: str, done: int, total: int) -> None:
        step = BUILD_STAGES.index(stage)
        text = STAGE_TEXT[stage]
        if stage == "load" and total:
            text = f"Membaca halaman {done} dari {total}"
        elif stage == "index" and total:
            text = f"Membuat vektor untuk {total} potongan dan menyimpan versi baru"
        hint = "Halaman hasil scan tanpa koreksi dibaca dengan OCR, bisa beberapa detik per halaman." if stage == "load" else ""
        box.markdown(theme.loading(text, step, len(BUILD_STAGES), hint), unsafe_allow_html=True)
        within = done / total if stage == "load" and total else 0.0
        bar.progress(min(1.0, (step + within) / len(BUILD_STAGES)))

    started = time.perf_counter()
    try:
        OcrService(student_page.get_config().tesseract_cmd, student_page.get_config().tesseract_lang).check_available()
        report = manager.initialize_knowledge_base(source, pages=pages, on_progress=progress)
    except tuple(BUILD_ERRORS) as exc:
        box.empty()
        bar.empty()
        reason = next(text for kind, text in BUILD_ERRORS.items() if isinstance(exc, kind))
        logger.error("Admin build failed: %s", type(exc).__name__)
        st.markdown(theme.report_box([
            "<b>Pembangunan gagal.</b> Knowledge base lama tetap dipakai mahasiswa.",
            escape(reason),
            f"<small>Rincian: {escape(str(exc))}</small>",
        ], failed=True), unsafe_allow_html=True)
        return None
    box.empty()
    bar.empty()
    st.session_state[REPORT_KEY] = (report, time.perf_counter() - started)
    return report


def render_report() -> None:
    saved = st.session_state.get(REPORT_KEY)
    if not saved:
        return
    report, seconds = saved
    lines = [
        f"<b>Knowledge base baru aktif</b> dalam {seconds:.0f} detik.",
        f"Buku: <b>{escape(report.source_file)}</b> · {report.page_count} halaman "
        f"({report.ocr_pages} OCR, {report.native_pages} teks digital) · {report.chunk_count} potongan",
        f"Versi: {escape(report.indexing.build_id)}",
    ]
    for warning in report.warnings:
        pages = warning.rsplit(":", 1)[-1].strip()
        lines.append(f"Perhatian: halaman OCR {escape(pages)} belum punya file koreksi. Pastikan teksnya sudah diperiksa.")
    st.markdown(theme.report_box(lines), unsafe_allow_html=True)


def save_upload(name: str, data: bytes, max_mb: int) -> Path:
    if len(data) > max_mb * 1024 * 1024:
        raise DocumentLoadError(f"File lebih dari {max_mb} MB")
    if not data.startswith(b"%PDF-"):
        raise DocumentLoadError("File bukan PDF")
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    safe = "".join(c if c.isalnum() or c in "-_." else "-" for c in Path(name).name)
    target = UPLOAD_DIR / f"{datetime.now():%Y%m%d-%H%M%S}-{safe}"
    target.write_bytes(data)
    return target


def render_replace(manager: ChatbotManager, config: AppConfig) -> None:
    st.caption("Buku baru dibangun di folder sementara dan baru dipakai setelah berhasil diperiksa. Kalau gagal, buku lama tetap dipakai.")
    upload = st.file_uploader("File buku pedoman (PDF)", type=["pdf"], key="pk-upload")
    pages_text = st.text_input("Halaman yang dipakai", value=config.knowledge_base_pages or "",
                               help="Contoh: 4-16,22-25,27-28. Kosongkan untuk memakai semua halaman.")
    approved = st.checkbox("Isi buku ini sudah disaring dan disetujui Product Owner")
    try:
        pages = parse_page_ranges(pages_text)
        page_error = None
    except ValueError:
        pages, page_error = None, "Format halaman tidak valid. Contoh: 4-16,22-25,27-28"
    if page_error:
        st.warning(page_error)
    columns = st.columns(2)
    build_new = columns[0].button("Bangun dari file baru", type="primary", key="pk-build-new",
                                  disabled=not (upload and approved) or bool(page_error), use_container_width=True)
    manifest = getattr(manager.vector_store, "manifest", None) or {}
    current = Path(manifest.get("source_path") or config.knowledge_base_path)
    rebuild = columns[1].button("Bangun ulang buku saat ini", key="pk-rebuild", disabled=bool(page_error) or not current.is_file(),
                                use_container_width=True, help=f"Memakai {current.name} dan halaman di atas")
    if build_new and upload:
        try:
            source = save_upload(upload.name, upload.getvalue(), config.pdf_max_upload_mb)
        except DocumentLoadError as exc:
            st.markdown(theme.report_box([f"<b>File ditolak.</b> {escape(str(exc))}."], failed=True), unsafe_allow_html=True)
            return
        if run_build(manager, source, pages) is None:
            source.unlink(missing_ok=True)
        else:
            st.rerun()
    elif rebuild and run_build(manager, current, pages):
        st.rerun()
    render_report()


# ---------- other tabs ----------

def render_versions(manager: ChatbotManager) -> None:
    store = manager.vector_store
    versions = store.versions() if hasattr(store, "versions") else []
    if not versions:
        st.info("Belum ada versi knowledge base.")
        return
    st.caption("Dua versi terakhir disimpan. Versi lama dapat diaktifkan kembali bila versi baru bermasalah.")
    for version in versions:
        created = datetime.fromisoformat(version["created_at"]).astimezone()
        name = version["sources"][0]["source_file"] if version.get("sources") else "?"
        detail = (f"{name} · halaman {student_page.page_ranges(version.get('pages', []))} · {version.get('chunk_count')} potongan · "
                  f"{version.get('embedding_model')}, {version.get('dimension')} dimensi")
        st.markdown(theme.version_row(f"{indonesian_date(created)}, {created:%H.%M}", detail, version["active"]), unsafe_allow_html=True)
        if not version["active"] and st.button("Aktifkan versi ini", key=f"pk-activate-{version['build_id']}"):
            try:
                store.activate_version(version["build_id"])
            except IndexNotReadyError as exc:
                st.error(f"Versi tidak dapat diaktifkan: {exc}")
            else:
                manager.clear_cache()
                st.toast("Versi lama aktif kembali.", icon=":material/history:")
                st.rerun()


def render_try(manager: ChatbotManager, config: AppConfig) -> None:
    st.caption("Mencoba pertanyaan seperti mahasiswa, lengkap dengan jarak potongan. Memakai kuota Gemini seperti biasa.")
    with st.form("pk-try", border=False):
        question = st.text_input("Pertanyaan uji", placeholder="Contoh: Berapa SKS minimal untuk ikut PKL?")
        sent = st.form_submit_button("Coba", type="primary")
    if not (sent and question.strip()):
        return
    box = st.empty()
    box.markdown(theme.loading("Menyiapkan jawaban"), unsafe_allow_html=True)
    started = time.perf_counter()
    response = manager.generate_response(question)
    box.empty()
    gate = config.retrieval_max_l2_distance
    distances = ", ".join(f"{d:.3f}" for d in response.distances) or "-"
    pages = ", ".join(str(p) for p in sorted({s.page for s in response.sources})) or "-"
    st.markdown(theme.key_values([
        ("Status", response.status.value),
        ("Waktu", f"{time.perf_counter() - started:.2f} detik"),
        ("Jarak potongan", f"{distances} (batas {gate if gate is not None else 'belum diatur'})"),
        ("Halaman rujukan", pages),
    ]), unsafe_allow_html=True)
    if response.status is ResponseStatus.ANSWERED:
        st.markdown(response.answer)
    else:
        st.info(response.answer)


def render_settings(manager: ChatbotManager, config: AppConfig) -> None:
    gate = config.retrieval_max_l2_distance
    st.markdown(theme.key_values([
        ("Model jawaban", config.gemini_chat_model),
        ("Batas waktu Gemini", f"{config.gemini_timeout_seconds:g} detik"),
        ("Model embedding", f"{config.gemini_embedding_model}, {config.embedding_output_dimension} dimensi"),
        ("Potongan teks", f"{config.chunk_size} karakter, tumpang tindih {config.chunk_overlap}"),
        ("Potongan per pertanyaan", str(config.retrieval_k)),
        ("Batas jarak relevansi", f"{gate}" if gate is not None else "belum diatur"),
        ("Panjang pertanyaan", f"maks. {config.question_max_chars} karakter"),
        ("Ukuran unggahan", f"maks. {config.pdf_max_upload_mb} MB"),
        ("Jawaban tersimpan", f"{manager.cached_answers()} pertanyaan"),
    ]), unsafe_allow_html=True)
    st.caption("Pengaturan diubah lewat file .env lalu website dijalankan ulang. Kata sandi dan API key tidak ditampilkan.")
    if st.button("Kosongkan jawaban tersimpan", key="pk-clear-cache", icon=":material/delete_sweep:"):
        manager.clear_cache()
        st.toast("Jawaban tersimpan dikosongkan.")
        st.rerun()


# ---------- dashboard ----------

def render_dashboard(user: str) -> None:
    left, right = st.columns([3, 1], vertical_alignment="center")
    left.markdown(f'<div class="pk-top">{theme.wordmark()}<span class="pk-pill"><i></i>ruang admin</span></div>', unsafe_allow_html=True)
    if right.button("Keluar", key="pk-logout", icon=":material/logout:", use_container_width=True):
        st.session_state.pop(AUTH_KEY, None)
        st.rerun()
    st.markdown(theme.admin_hello(user), unsafe_allow_html=True)

    manager, problem = student_page.load_manager()
    if manager is None:
        st.error(problem)
        return
    config = student_page.get_config()
    store = manager.vector_store
    manifest = getattr(store, "manifest", None)
    if manifest:
        name = manifest["sources"][0]["source_file"] if manifest.get("sources") else "?"
        versions = store.versions() if hasattr(store, "versions") else []
        created = datetime.fromisoformat(manifest["created_at"]).astimezone()
        st.markdown(theme.stats([
            ("Buku aktif", student_page.document_name(name), f"sha256 {manifest['sources'][0]['source_hash'][:12]}" if manifest.get("sources") else ""),
            ("Halaman", str(len(manifest["pages"])), student_page.page_ranges(manifest["pages"])),
            ("Potongan", str(manifest["chunk_count"]), f"{manifest['dimension']} dimensi"),
            ("Versi", str(len(versions)), f"aktif sejak {indonesian_date(created)}"),
        ]), unsafe_allow_html=True)
        st.markdown(theme.label("Peta halaman buku"), unsafe_allow_html=True)
        st.markdown(theme.page_map(store.total_pages(), store.chunks_per_page()), unsafe_allow_html=True)
    else:
        st.warning(problem or "Knowledge base belum dibangun.", icon=":material/info:")

    st.write("")
    tabs = st.tabs(["Ganti buku pedoman", "Riwayat versi", "Uji pertanyaan", "Pengaturan"])
    with tabs[0]:
        render_replace(manager, config)
    with tabs[1]:
        render_versions(manager)
    with tabs[2]:
        render_try(manager, config)
    with tabs[3]:
        render_settings(manager, config)


def main() -> None:
    st.markdown(theme.style(), unsafe_allow_html=True)
    try:
        config = student_page.get_config()
    except Exception:  # invalid .env values
        logger.exception("Configuration could not be read")
        st.error("Pengaturan Pekael tidak valid. Periksa file .env.")
        return
    user = st.session_state.get(AUTH_KEY)
    if user:
        render_dashboard(user)
    else:
        render_login(config)
