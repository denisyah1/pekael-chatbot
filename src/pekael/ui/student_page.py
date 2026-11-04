"""Student question page (spec §12 Sprint 4, FR-01, FR-05, FR-08, FR-10, NFR-05).

Plain academic look: a question box, the answer, and the handbook pages it came from.
Questions and answers stay visible only for the current browser session and are never
sent back to the model (no conversation memory).
"""

import logging
from dataclasses import dataclass
from pathlib import Path

import streamlit as st

from pekael.config.app_configurator import AppConfigurator
from pekael.config.logging_config import configure_logging
from pekael.config.settings import AppConfig, ConfigError
from pekael.core.chatbot_manager import ChatbotManager
from pekael.core.schemas import ChatbotResponse, ResponseStatus, SourceReference
from pekael.models.embeddings import EmbeddingError
from pekael.models.gemini_model import LLMError
from pekael.vectorstores.base import IndexNotReadyError

logger = logging.getLogger(__name__)

TITLE = "Pekael"
SUBTITLE = (
    "Layanan informasi Praktik Kerja Lapangan (PKL) Prodi Pendidikan Teknik Informatika dan Komputer, "
    "Universitas Negeri Jakarta. Jawaban disusun dari Buku Pedoman PKL."
)
PLACEHOLDER = "Contoh: Berapa SKS minimal untuk bisa mengikuti PKL?"
NOTE = (
    "Jawaban disusun dari buku pedoman dan dapat keliru. Untuk keputusan resmi, "
    "periksa buku pedoman atau hubungi koordinator PKL."
)
NOT_CONFIGURED = "Layanan Pekael belum dapat digunakan karena pengaturan belum lengkap. Silakan hubungi admin."
NOT_READY = "Buku pedoman belum dimuat ke Pekael, sehingga pertanyaan belum dapat dijawab. Silakan hubungi admin."
HISTORY_KEY = "history"


@dataclass(frozen=True)
class Exchange:
    question: str
    response: ChatbotResponse


@st.cache_resource(show_spinner=False)
def get_config() -> AppConfig:
    config = AppConfigurator.read_config()
    configure_logging(config.log_level, config.secret_values())
    return config


@st.cache_resource(show_spinner=False)
def get_manager() -> ChatbotManager:
    """One manager per server process, so the FAISS index is loaded once and shared."""
    return AppConfigurator.create_manager_from_config(get_config())


def document_name(source_file: str) -> str:
    """'Pedoman-PKL-2025.pdf' -> 'Pedoman PKL 2025'."""
    return Path(source_file).stem.replace("-", " ").replace("_", " ")


def pages_line(sources: tuple[SourceReference, ...]) -> str:
    by_document: dict[str, list[int]] = {}
    for source in sources:
        pages = by_document.setdefault(document_name(source.source_file), [])
        if source.page not in pages:
            pages.append(source.page)
    parts = [f"{name}, halaman PDF {', '.join(str(p) for p in sorted(pages))}" for name, pages in by_document.items()]
    return "Sumber: " + " · ".join(parts)


def render_sources(sources: tuple[SourceReference, ...]) -> None:
    st.caption(pages_line(sources))
    with st.expander("Lihat kutipan dari buku pedoman"):
        for source in sources:
            heading = f"Halaman PDF {source.page}"
            if source.section:
                heading += f" · {source.section}"
            st.markdown(f"**{heading}**")
            st.caption(source.snippet or "")


def render_exchange(item: Exchange) -> None:
    with st.container(border=True):
        st.markdown(f"**{item.question}**")
        status = item.response.status
        if status is ResponseStatus.ANSWERED:
            st.markdown(item.response.answer)
            if item.response.sources:
                render_sources(item.response.sources)
        elif status is ResponseStatus.OUT_OF_SCOPE:
            st.info(item.response.answer)
        else:
            st.warning(item.response.answer)


def load_manager() -> tuple[ChatbotManager | None, str | None]:
    """Return the manager, or a message explaining why questions cannot be answered yet."""
    try:
        manager = get_manager()
    except (ConfigError, EmbeddingError, LLMError) as exc:  # e.g. GEMINI_API_KEY not set
        logger.error("Pekael is not configured: %s", type(exc).__name__)
        return None, NOT_CONFIGURED
    if getattr(manager.vector_store, "is_ready", False):
        return manager, None
    try:
        manager.vector_store.load()
    except IndexNotReadyError as exc:
        logger.warning("Knowledge base not ready: %s", exc)
        return manager, NOT_READY
    return manager, None


def main() -> None:
    st.set_page_config(page_title="Pekael · Informasi PKL PTIK UNJ", page_icon=":material/menu_book:", layout="centered")
    st.title(TITLE)
    st.write(SUBTITLE)

    manager, problem = load_manager()
    history: list[Exchange] = st.session_state.setdefault(HISTORY_KEY, [])
    max_chars = get_config().question_max_chars if manager else 500  # config may be invalid

    with st.form("question_form", clear_on_submit=True, border=False):
        question = st.text_area(
            "Pertanyaan tentang PKL",
            placeholder=PLACEHOLDER,
            max_chars=max_chars,
            height=100,
            disabled=problem is not None,
        )
        sent = st.form_submit_button("Kirim", type="primary", disabled=problem is not None)

    if problem:
        st.warning(problem)
    elif sent:
        with st.spinner("Mencari jawaban di buku pedoman..."):
            response = manager.generate_response(question)
        if response.status is ResponseStatus.INVALID_INPUT:
            st.warning(response.answer)
        else:
            history.insert(0, Exchange(question.strip(), response))

    for item in history:
        render_exchange(item)

    if history and st.button("Hapus riwayat", type="tertiary"):
        history.clear()
        st.rerun()

    st.divider()
    st.caption(NOTE)
