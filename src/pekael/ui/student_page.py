"""Student question page (spec §12 Sprint 4, FR-01, FR-05, FR-08, FR-10, NFR-05).

Flow: intro ("PKL, dibaca pe·ka·el") -> question page with examples and handbook facts ->
answers with the handbook pages they came from. Every wait shows what Pekael is doing.
Questions and answers stay visible only for the current browser session and are never
sent back to the model (no conversation memory).
"""

import logging
import random
from html import escape
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import streamlit as st

from pekael.config.app_configurator import AppConfigurator
from pekael.config.logging_config import configure_logging
from pekael.config.settings import AppConfig, ConfigError
from pekael.core.chatbot_manager import ChatbotManager
from pekael.core.schemas import ChatbotResponse, ResponseStatus, SourceReference
from pekael.models.embeddings import EmbeddingError
from pekael.models.gemini_model import LLMError
from pekael.ui import content, theme
from pekael.vectorstores.base import IndexNotReadyError

logger = logging.getLogger(__name__)

HISTORY_KEY = "history"
INTRO_KEY = "intro_done"
NOTICE_KEY = "notice"
BOOTED_KEY = "booted"
MONTHS = ("Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember")


@dataclass(frozen=True)
class Exchange:
    question: str
    response: ChatbotResponse
    asked_at: str = ""  # "14.02", shown under the bubbles
    answered_at: str = ""


def clock() -> str:
    return datetime.now().strftime("%H.%M")


@st.cache_resource(show_spinner=False)
def get_config() -> AppConfig:
    config = AppConfigurator.read_config()
    configure_logging(config.log_level, config.secret_values())
    return config


@st.cache_resource(show_spinner=False)
def get_manager() -> ChatbotManager:
    """One manager per server process, so the FAISS index is loaded once and shared."""
    return AppConfigurator.create_manager_from_config(get_config())


def load_manager() -> tuple[ChatbotManager | None, str | None]:
    """Return the manager, or a message explaining why questions cannot be answered yet."""
    try:
        manager = get_manager()
    except (ConfigError, EmbeddingError, LLMError) as exc:  # e.g. GEMINI_API_KEY not set
        logger.error("Pekael is not configured: %s", type(exc).__name__)
        return None, content.NOT_CONFIGURED
    if getattr(manager.vector_store, "is_ready", False):
        return manager, None
    try:
        manager.vector_store.load()
    except IndexNotReadyError as exc:
        logger.warning("Knowledge base not ready: %s", exc)
        return manager, content.NOT_READY
    return manager, None


# ---------- formatting ----------

def document_name(source_file: str) -> str:
    """'Pedoman-PKL-2025.pdf' -> 'Pedoman PKL 2025'."""
    return Path(source_file).stem.replace("-", " ").replace("_", " ")


def page_ranges(pages: list[int]) -> str:
    """[4, 5, 6, 9] -> '4–6, 9'."""
    ranges: list[list[int]] = []
    for page in sorted(set(pages)):
        if ranges and page == ranges[-1][1] + 1:
            ranges[-1][1] = page
        else:
            ranges.append([page, page])
    return ", ".join(f"{a}–{b}" if a != b else str(a) for a, b in ranges)


def readable_date(iso: str) -> str:
    moment = datetime.fromisoformat(iso).astimezone()  # local time (WIB), as in the admin room
    return f"{moment.day} {MONTHS[moment.month - 1]} {moment.year}"


def source_pages(sources: tuple[SourceReference, ...]) -> list[int]:
    return sorted({s.page for s in sources})


# ---------- sections ----------

def render_intro() -> None:
    slot = st.empty()
    with slot.container():
        st.markdown(theme.intro(), unsafe_allow_html=True)
        started = st.button("Mulai bertanya", key="pk-start")
    if started:
        slot.empty()  # remove the intro at once, so only the loading screen shows
        st.session_state[INTRO_KEY] = True
        st.rerun()


def render_sidebar(manager: ChatbotManager | None) -> None:
    manifest = getattr(manager.vector_store, "manifest", None) if manager else None
    with st.sidebar:
        st.markdown(theme.wordmark(), unsafe_allow_html=True)
        steps = "".join(
            f'<div class="pk-step"><b>{i}</b><div><strong>{title}</strong>{text}</div></div>'
            for i, (title, text) in enumerate(content.HOW_IT_WORKS, start=1)
        )
        st.markdown(f'<div class="pk-side"><h4>Cara kerja</h4>{steps}<h4>Sumber jawaban</h4></div>', unsafe_allow_html=True)
        if manifest:
            name = document_name(manifest["sources"][0]["source_file"]) if manifest.get("sources") else "Buku pedoman"
            st.markdown(
                f'<div class="pk-src"><strong>{escape(name)}</strong><br>Halaman PDF {page_ranges(manifest["pages"])}<br>'
                f'{manifest["chunk_count"]} potongan teks · dimuat {readable_date(manifest["created_at"])}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown('<div class="pk-src">Buku pedoman belum dimuat.</div>', unsafe_allow_html=True)
        st.write("")
        if st.button("Percakapan baru", key="pk-clear", icon=":material/refresh:", use_container_width=True):
            st.session_state[HISTORY_KEY] = []
            st.rerun()
        if st.button("Putar intro lagi", key="pk-replay", icon=":material/play_circle:", type="tertiary"):
            st.session_state[INTRO_KEY] = False
            st.rerun()
        st.markdown('<div class="pk-back" style="text-align:left"><a href="admin" target="_self">Masuk ruang admin →</a></div>',
                    unsafe_allow_html=True)


def render_welcome(disabled: bool) -> str | None:
    """Greeting, example questions and handbook facts. Returns a clicked example question."""
    st.markdown(theme.greeting(content.GREETING, content.GREETING_SUB), unsafe_allow_html=True)
    st.markdown(theme.label("Coba tanyakan"), unsafe_allow_html=True)
    chosen = None
    columns = st.columns(2)
    for i, example in enumerate(content.EXAMPLES):
        with columns[i % 2]:
            if st.button(example, key=f"pk-ex-{i}", disabled=disabled, use_container_width=True):
                chosen = example
    st.markdown(theme.label("Sekilas PKL"), unsafe_allow_html=True)
    st.markdown(theme.facts_grid(), unsafe_allow_html=True)
    return chosen


def render_exchange(index: int, item: Exchange) -> None:
    st.markdown(theme.question_bubble(item.question, item.asked_at), unsafe_allow_html=True)
    response = item.response
    if response.status is ResponseStatus.ANSWERED:
        with st.container(key=f"pk-a-{index}"):
            st.markdown('<div class="pk-from">Dari buku pedoman</div>', unsafe_allow_html=True)
            st.markdown(response.answer)
            if response.sources:
                document = document_name(response.sources[0].source_file)
                st.markdown(theme.page_tabs(source_pages(response.sources), document), unsafe_allow_html=True)
                with st.expander("Lihat kutipan dari buku pedoman"):
                    for source in response.sources:
                        st.markdown(theme.quote(source.page, source.section, source.snippet), unsafe_allow_html=True)
            st.markdown(theme.time_stamp(item.answered_at), unsafe_allow_html=True)
    else:
        warn = response.status is not ResponseStatus.OUT_OF_SCOPE
        label = "Perlu dicoba lagi" if warn else "Tidak ada di buku pedoman"
        with st.container(key=f"pk-a-out-{index}"):
            st.markdown(f'<div class="pk-from">{label}</div>', unsafe_allow_html=True)
            css = "pk-status pk-warn" if warn else "pk-status"
            st.markdown(f'<div class="{css}">{escape(response.answer)}</div>', unsafe_allow_html=True)
            st.markdown(theme.time_stamp(item.answered_at), unsafe_allow_html=True)


def answer(manager: ChatbotManager, question: str, history: list[Exchange]) -> None:
    asked_at = clock()
    st.markdown(theme.question_bubble(question, asked_at), unsafe_allow_html=True)
    placeholder = st.empty()
    names = list(content.STEP_LABELS)
    fact = random.choice(content.FACTS)
    hint = f"Sambil menunggu: {fact.figure}, {fact.text[0].lower()}{fact.text[1:-1]} (hal. {fact.page})"

    def report(step: str) -> None:
        note = content.SLOW_HINT if step == "generate" else hint
        placeholder.markdown(theme.loading(content.STEP_LABELS[step], names.index(step), len(names), note), unsafe_allow_html=True)

    report(names[0])
    response = manager.generate_response(question, on_step=report)
    placeholder.empty()
    if response.status is ResponseStatus.INVALID_INPUT:
        st.session_state[NOTICE_KEY] = response.answer
    else:
        history.append(Exchange(question.strip(), response, asked_at, clock()))
    st.rerun()


def main() -> None:
    st.markdown(theme.style(), unsafe_allow_html=True)

    if not st.session_state.get(INTRO_KEY):
        render_intro()
        return

    boot = st.empty()
    if not st.session_state.get(BOOTED_KEY):  # only the first page view waits for the handbook
        boot.markdown(theme.boot(), unsafe_allow_html=True)
    manager, problem = load_manager()
    boot.empty()
    st.session_state[BOOTED_KEY] = True

    render_sidebar(manager)
    manifest = getattr(manager.vector_store, "manifest", None) if manager and not problem else None
    pill = f"{document_name(manifest['sources'][0]['source_file'])} · {len(manifest['pages'])} halaman" if manifest else "Buku pedoman belum siap"
    st.markdown(theme.top_bar(pill, problem is None), unsafe_allow_html=True)

    history: list[Exchange] = st.session_state.setdefault(HISTORY_KEY, [])
    if problem:
        st.warning(problem, icon=":material/info:")

    chosen = render_welcome(problem is not None) if not history else None
    for index, item in enumerate(history):
        render_exchange(index, item)

    notice = st.session_state.pop(NOTICE_KEY, None)
    if notice:
        st.toast(notice, icon=":material/edit_note:")

    max_chars = get_config().question_max_chars if manager else 500  # config may be invalid
    typed = st.chat_input(content.PLACEHOLDER, max_chars=max_chars, disabled=problem is not None, submit_mode="disable")
    question = typed or chosen
    if question and manager and not problem:
        answer(manager, question, history)

    st.markdown(f'<div class="pk-note">{escape(content.NOTE)}</div>', unsafe_allow_html=True)
