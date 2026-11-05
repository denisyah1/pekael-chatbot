"""Visual identity of the student page: palette, typography, wordmark, intro and loaders.

Concept: "PKL, dibaca pe·ka·el". The wordmark starts as the three letters p k l and the
spoken vowels grow in between them in a softer italic face. Floating page numbers and
faint ruled lines refer to the handbook pages every answer is tied to.

All HTML here is static or built from escaped text; it is rendered with
``st.markdown(unsafe_allow_html=True)``, which does not run JavaScript.
"""

from html import escape

from pekael.ui.content import FACTS, INTRO_LINES, Fact

FONTS = (
    "https://fonts.googleapis.com/css2?"
    "family=Fraunces:ital,opsz,wght,SOFT,WONK@1,9..144,300..600,0..100,0..1"
    "&family=Plus+Jakarta+Sans:wght@400..800&display=swap"
)

CSS = """
@import url('__FONTS__');

:root {
  --pk-bg: #0A1222;
  --pk-bg-deep: #060C18;
  --pk-surface: #111C31;
  --pk-raised: #17243D;
  --pk-line: #22324F;
  --pk-slate: #7D90AE;
  --pk-slate-soft: #A6B4CB;
  --pk-text: #E7ECF4;
  --pk-tint: #C8D7FF;
  --pk-tint-deep: #8FA9EC;
  --pk-sand: #F1D9B8;
  --pk-sans: "Plus Jakarta Sans", -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", system-ui, sans-serif;
  --pk-serif: "Fraunces", "Iowan Old Style", Georgia, serif;
  --pk-radius: 18px;
}

html, body, .stApp, p, li, label, h1, h2, h3, h4, button, input, textarea,
[data-testid="stChatInput"] textarea, [data-testid="stExpander"] summary p,
[data-testid="stMarkdownContainer"] :is(div, span, strong, em, b, small, i, u, section) {
  font-family: var(--pk-sans) !important;
}
/* serif accents (more specific than the rule above) */
.stApp .pk-word .pk-v, .stApp .pk-spoken b, .stApp .pk-hello .pk-soft, .stApp .pk-admin-hello .pk-soft, .stApp .pk-intro .pk-float {
  font-family: var(--pk-serif) !important;
}

.stApp {
  background:
    radial-gradient(60rem 40rem at 85% -10%, rgba(143, 169, 236, 0.10), transparent 60%),
    radial-gradient(50rem 36rem at -10% 110%, rgba(125, 144, 174, 0.10), transparent 60%),
    var(--pk-bg);
}
header[data-testid="stHeader"] { background: transparent; }
[data-testid="stBottom"] > div { background: linear-gradient(to top, var(--pk-bg) 70%, transparent); }
[data-testid="stSidebar"] { background: var(--pk-bg-deep); border-right: 1px solid var(--pk-line); }
.block-container { padding-top: 2.2rem; max-width: 46rem; }

/* ---------- wordmark ---------- */
.pk-word { display: inline-flex; align-items: baseline; color: var(--pk-text); line-height: 1; user-select: none; }
.pk-word .pk-c { font-family: var(--pk-sans); font-weight: 800; letter-spacing: -0.04em; }
.pk-word .pk-v {
  font-family: var(--pk-serif); font-style: italic; font-weight: 400; color: var(--pk-tint);
  font-variation-settings: "SOFT" 100, "WONK" 1, "opsz" 144; display: inline-block;
}
.pk-word .pk-v2 { transform: translateY(-0.06em) rotate(-4deg); color: var(--pk-sand); }
.pk-word .pk-v3 { transform: translateY(0.03em); }
.pk-word--small { font-size: 1.65rem; }
.pk-word--small .pk-v { margin: 0 0.01em; }

/* ---------- intro ---------- */
.pk-intro {
  position: relative; min-height: 64vh; display: flex; flex-direction: column; align-items: center;
  justify-content: center; text-align: center; overflow: hidden; padding: 2rem 0 1rem;
}
.pk-intro::before {
  content: ""; position: absolute; inset: 0; z-index: 0; pointer-events: none;
  background: repeating-linear-gradient(to bottom, transparent 0 41px, rgba(166, 180, 203, 0.06) 41px 42px);
  mask-image: radial-gradient(ellipse at center, black 30%, transparent 75%);
}
.pk-intro > * { position: relative; z-index: 1; }
.pk-kicker {
  font-size: 0.78rem; letter-spacing: 0.32em; text-transform: uppercase; color: var(--pk-slate);
  opacity: 0; animation: pk-fade 0.8s ease 0.2s forwards;
}
.pk-word--hero { font-size: clamp(4.2rem, 17vw, 8.5rem); margin: 0.6rem 0 0.2rem; }
.pk-word--hero .pk-c { margin: 0 0.32em; animation: pk-close 1.3s cubic-bezier(.7, 0, .2, 1) 1.5s forwards; }
.pk-word--hero .pk-v { max-width: 0; opacity: 0; vertical-align: baseline; }
.pk-word--hero .pk-v1 { animation: pk-grow 1.1s cubic-bezier(.2, .8, .2, 1) 1.6s forwards; }
.pk-word--hero .pk-v2 { animation: pk-grow 1.1s cubic-bezier(.2, .8, .2, 1) 1.8s forwards; }
.pk-word--hero .pk-v3 { animation: pk-grow 1.1s cubic-bezier(.2, .8, .2, 1) 2.0s forwards; }
.pk-stroke { width: min(20rem, 70vw); height: 1.6rem; margin-top: -0.4rem; }
.pk-stroke path {
  fill: none; stroke: var(--pk-tint-deep); stroke-width: 2.2; stroke-linecap: round;
  stroke-dasharray: 420; stroke-dashoffset: 420; animation: pk-draw 1.4s ease 2.7s forwards;
}
.pk-spoken { font-size: 0.95rem; color: var(--pk-slate); opacity: 0; animation: pk-fade 0.8s ease 2.9s forwards; }
.pk-spoken b { font-family: var(--pk-serif); font-style: italic; font-weight: 400; color: var(--pk-tint); }
.pk-lines { margin-top: 1.6rem; }
.pk-lines p { margin: 0.25rem 0; color: var(--pk-slate-soft); opacity: 0; animation: pk-rise 0.9s ease forwards; }
.pk-lines p:first-child { font-size: 1.15rem; color: var(--pk-text); font-weight: 600; animation-delay: 3.4s; }
.pk-lines p:last-child { animation-delay: 3.8s; max-width: 30rem; }

.pk-ticker {
  position: relative; height: 3.4rem; width: min(30rem, 90vw); margin: 1.8rem auto 0;
  opacity: 0; animation: pk-fade 0.8s ease 4.3s forwards;
}
.pk-ticker .pk-tick {
  position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; gap: 0.7rem;
  opacity: 0; animation: pk-cycle 24s ease infinite; color: var(--pk-slate-soft); font-size: 0.92rem;
}
.pk-tick span { text-align: left; }
.pk-tick strong { color: var(--pk-sand); font-weight: 700; white-space: nowrap; }
.pk-tick em { font-style: normal; font-size: 0.72rem; color: var(--pk-slate); border: 1px solid var(--pk-line); border-radius: 99px; padding: 0.1rem 0.5rem; white-space: nowrap; }

.pk-float { position: absolute; z-index: 0 !important; font-family: var(--pk-serif); font-style: italic; color: rgba(166, 180, 203, 0.16); animation: pk-drift linear infinite; pointer-events: none; }

.st-key-pk-start { width: 100%; opacity: 0; animation: pk-fade 0.8s ease 4.6s forwards; }
.st-key-pk-start [data-testid="stButton"] { display: flex; justify-content: center; }
.st-key-pk-start [data-testid="stButton"] > *, .st-key-pk-start button { width: auto !important; }
.st-key-pk-start button {
  background: var(--pk-tint) !important; color: var(--pk-bg) !important; border: 0 !important;
  border-radius: 99px !important; padding: 0.7rem 1.9rem !important; font-weight: 700 !important;
  box-shadow: 0 10px 34px rgba(143, 169, 236, 0.25); transition: transform .2s ease, box-shadow .2s ease;
}
.st-key-pk-start button:hover { transform: translateY(-2px); box-shadow: 0 14px 40px rgba(143, 169, 236, 0.35); }
.st-key-pk-start button p { font-size: 1rem !important; }

/* ---------- main page ---------- */
.pk-enter { animation: pk-rise 0.7s ease both; }
.pk-top { display: flex; align-items: center; justify-content: space-between; gap: 1rem; margin-bottom: 1.6rem; }
.pk-pill { font-size: 0.75rem; color: var(--pk-slate-soft); border: 1px solid var(--pk-line); background: var(--pk-surface); border-radius: 99px; padding: 0.3rem 0.8rem; white-space: nowrap; }
.pk-pill i { font-style: normal; display: inline-block; width: 0.45rem; height: 0.45rem; border-radius: 50%; background: #7FD1A8; margin-right: 0.4rem; box-shadow: 0 0 0 3px rgba(127, 209, 168, 0.15); }
.pk-pill.pk-off i { background: var(--pk-sand); box-shadow: 0 0 0 3px rgba(241, 217, 184, 0.15); }
.pk-hello .pk-h { font-size: clamp(1.7rem, 5.4vw, 2.2rem); font-weight: 800; letter-spacing: -0.03em; line-height: 1.15; margin: 0 0 0.5rem; color: var(--pk-text); }
.pk-hello .pk-soft { font-family: var(--pk-serif); font-style: italic; font-weight: 400; letter-spacing: -0.01em; color: var(--pk-tint); font-variation-settings: "SOFT" 100, "WONK" 1; }
.pk-hello p { color: var(--pk-slate-soft); margin: 0 0 1.4rem; }
.pk-label { font-size: 0.72rem; letter-spacing: 0.22em; text-transform: uppercase; color: var(--pk-slate); margin: 1.6rem 0 0.7rem; }

[class*="st-key-pk-ex-"] button {
  width: 100%; justify-content: flex-start; text-align: left; min-height: 3.1rem;
  background: var(--pk-surface) !important; border: 1px solid var(--pk-line) !important; border-radius: 14px !important;
  color: var(--pk-text) !important; transition: border-color .2s ease, transform .2s ease, background .2s ease;
}
[class*="st-key-pk-ex-"] button:hover { border-color: var(--pk-tint-deep) !important; background: var(--pk-raised) !important; transform: translateY(-1px); }
[class*="st-key-pk-ex-"] button > div { justify-content: flex-start; width: 100%; }
[class*="st-key-pk-ex-"] button p { font-size: 0.9rem !important; text-align: left; white-space: normal !important; overflow: visible !important; text-overflow: clip !important; }

.pk-facts { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 0.7rem; }
@media (max-width: 640px) { .pk-facts { grid-template-columns: repeat(2, minmax(0, 1fr)); } .pk-top { flex-wrap: wrap; } }
.pk-fact { background: var(--pk-surface); border: 1px solid var(--pk-line); border-radius: 16px; padding: 0.9rem 0.95rem 0.8rem; display: flex; flex-direction: column; gap: 0.35rem; }
.pk-fact strong { font-size: 1.25rem; font-weight: 800; color: var(--pk-sand); letter-spacing: -0.02em; }
.pk-fact span { font-size: 0.8rem; color: var(--pk-slate-soft); line-height: 1.35; flex: 1; }
.pk-fact em { font-style: normal; font-size: 0.68rem; color: var(--pk-slate); align-self: flex-start; border: 1px solid var(--pk-line); border-radius: 99px; padding: 0.05rem 0.45rem; }

.pk-q { display: flex; justify-content: flex-end; margin: 1.4rem 0 0.6rem; animation: pk-rise 0.4s ease both; }
.pk-q div { max-width: 85%; background: var(--pk-tint); color: var(--pk-bg); padding: 0.65rem 1rem; border-radius: 18px 18px 4px 18px; font-weight: 600; font-size: 0.95rem; line-height: 1.45; }

[class*="st-key-pk-a-"] {
  background: var(--pk-surface); border: 1px solid var(--pk-line); border-radius: 4px 20px 20px 20px;
  padding: 1rem 1.15rem 0.6rem; animation: pk-rise 0.5s ease both;
}
[class*="st-key-pk-a-out"] { border-style: dashed; background: transparent; }
.pk-from { font-size: 0.72rem; letter-spacing: 0.18em; text-transform: uppercase; color: var(--pk-slate); margin-bottom: 0.2rem; }
.pk-pages { display: flex; flex-wrap: wrap; gap: 0.4rem; align-items: center; margin: 0.3rem 0 0.1rem; }
.pk-pages small { color: var(--pk-slate); font-size: 0.75rem; margin-right: 0.2rem; }
.pk-page { font-size: 0.75rem; font-weight: 600; color: var(--pk-tint); background: rgba(200, 215, 255, 0.08); border: 1px solid rgba(200, 215, 255, 0.22); border-radius: 8px 8px 8px 2px; padding: 0.12rem 0.55rem; }
.pk-status { color: var(--pk-slate-soft); }
.pk-status.pk-warn { color: var(--pk-sand); }
[data-testid="stExpander"] details { border-color: var(--pk-line) !important; border-radius: 12px !important; background: transparent; }
.pk-quote { border-left: 2px solid var(--pk-tint-deep); padding: 0.1rem 0 0.1rem 0.8rem; margin: 0.4rem 0 0.9rem; }
.pk-quote b { display: block; font-size: 0.78rem; color: var(--pk-tint); font-weight: 600; margin-bottom: 0.2rem; }
.pk-quote span { font-size: 0.85rem; color: var(--pk-slate-soft); line-height: 1.5; }

/* ---------- loading ---------- */
.pk-loading { display: flex; align-items: center; gap: 0.9rem; padding: 0.9rem 1.1rem; background: var(--pk-surface); border: 1px solid var(--pk-line); border-radius: 4px 20px 20px 20px; margin-bottom: 0.6rem; }
.pk-book { position: relative; width: 2rem; height: 1.45rem; flex: none; perspective: 80px; }
.pk-book::before, .pk-book::after, .pk-book i { content: ""; position: absolute; top: 0; width: 50%; height: 100%; border: 2px solid var(--pk-tint-deep); }
.pk-book::before { left: 0; border-radius: 4px 0 0 4px; border-right-width: 1px; }
.pk-book::after { right: 0; border-radius: 0 4px 4px 0; border-left-width: 1px; }
.pk-book i { right: 0; border-color: var(--pk-tint); border-radius: 0 4px 4px 0; transform-origin: left center; animation: pk-flip 1.1s ease-in-out infinite; background: var(--pk-surface); }
.pk-loading-text { display: flex; flex-direction: column; gap: 0.15rem; }
.pk-loading-text b { font-weight: 600; color: var(--pk-text); font-size: 0.92rem; }
.pk-loading-text span { font-size: 0.75rem; color: var(--pk-slate); }
.pk-dots::after { content: ""; animation: pk-dots 1.4s steps(4) infinite; }
.pk-steps { display: flex; gap: 0.3rem; margin-top: 0.35rem; }
.pk-steps u { text-decoration: none; display: block; width: 1.3rem; height: 3px; border-radius: 3px; background: var(--pk-line); }
.pk-steps u.on { background: var(--pk-tint-deep); }
.pk-steps u.now { background: linear-gradient(90deg, var(--pk-line), var(--pk-tint), var(--pk-line)); background-size: 200% 100%; animation: pk-shimmer 1.2s linear infinite; }
.pk-boot { min-height: 50vh; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 1.2rem; color: var(--pk-slate-soft); }
.pk-boot .pk-word--small { animation: pk-breathe 2s ease-in-out infinite; }

/* ---------- sidebar ---------- */
.pk-side h4 { font-size: 0.72rem; letter-spacing: 0.22em; text-transform: uppercase; color: var(--pk-slate); margin: 1.4rem 0 0.6rem; font-weight: 600; }
.pk-step { display: flex; gap: 0.7rem; margin-bottom: 0.8rem; }
.pk-step b { flex: none; width: 1.5rem; height: 1.5rem; border-radius: 50%; display: grid; place-items: center; font-size: 0.75rem; background: var(--pk-raised); color: var(--pk-tint); border: 1px solid var(--pk-line); }
.pk-step div { font-size: 0.82rem; color: var(--pk-slate-soft); line-height: 1.4; }
.pk-step div strong { display: block; color: var(--pk-text); font-weight: 600; }
.pk-src { font-size: 0.82rem; color: var(--pk-slate-soft); background: var(--pk-surface); border: 1px solid var(--pk-line); border-radius: 14px; padding: 0.8rem 0.9rem; line-height: 1.55; }
.pk-src strong { color: var(--pk-text); }
.pk-note { font-size: 0.75rem; color: var(--pk-slate); text-align: center; margin-top: 2rem; }

/* ---------- chat columns (question right, answer left) ---------- */
.pk-q { flex-direction: column; align-items: flex-end; margin: 1.3rem 0 0.5rem; }
.pk-q div { max-width: min(78%, 34rem); }
.pk-time { font-size: 0.68rem; color: var(--pk-slate); margin-top: 0.25rem; }
.pk-q .pk-time { padding-right: 0.3rem; }
[class*="st-key-pk-a-"] { width: fit-content !important; max-width: min(86%, 38rem) !important; margin-right: auto; }
[class*="st-key-pk-a-"] .pk-time { text-align: right; margin: 0.1rem 0 0.2rem; }
.pk-loading { width: fit-content; max-width: min(86%, 38rem); }
@media (max-width: 640px) { [class*="st-key-pk-a-"] { max-width: 92% !important; } .pk-q div { max-width: 88%; } }

/* ---------- admin: library card login ---------- */
.pk-card-wrap { max-width: 27rem; margin: 5vh auto 0; }
.pk-card {
  position: relative; overflow: hidden; background: var(--pk-surface); border: 1px solid var(--pk-line); border-bottom: 0;
  border-radius: 22px 22px 0 0; padding: 1.5rem 1.6rem 1rem 2.1rem;
  background-image: repeating-linear-gradient(to bottom, transparent 0 27px, rgba(166, 180, 203, 0.07) 27px 28px);
}
.pk-card::before { content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 7px; background: linear-gradient(var(--pk-tint), var(--pk-tint-deep) 55%, var(--pk-sand)); }
.pk-card::after { content: ""; position: absolute; right: 1.3rem; top: 1.25rem; width: 0.85rem; height: 0.85rem; border-radius: 50%; background: var(--pk-bg); box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.6); }
.pk-card-kicker { font-size: 0.68rem; letter-spacing: 0.28em; text-transform: uppercase; color: var(--pk-slate); }
.pk-card-title { display: flex; align-items: baseline; gap: 0.55rem; margin: 0.35rem 0 0.15rem; }
.pk-card-title .pk-word { font-size: 2.1rem; }
.pk-card-title em { font-family: var(--pk-serif); font-style: italic; color: var(--pk-sand); font-size: 1.35rem; }
.pk-card-sub { color: var(--pk-slate-soft); font-size: 0.85rem; margin-bottom: 0.9rem; }
.pk-card-row { display: flex; justify-content: space-between; font-size: 0.72rem; color: var(--pk-slate); border-top: 1px dashed var(--pk-line); padding-top: 0.55rem; letter-spacing: 0.08em; }
.pk-stamp {
  position: absolute; right: 1.1rem; bottom: 2.6rem; transform: rotate(-11deg); border: 2px dashed rgba(241, 217, 184, 0.55);
  color: rgba(241, 217, 184, 0.75); font-size: 0.62rem; font-weight: 800; letter-spacing: 0.22em; padding: 0.3rem 0.6rem; border-radius: 6px;
  animation: pk-stamp 0.6s cubic-bezier(.2, 1.6, .4, 1) 0.4s both;
}
.st-key-pk-login { max-width: 27rem; margin: 0 auto; background: var(--pk-surface); border: 1px solid var(--pk-line); border-top: 0; border-radius: 0 0 22px 22px; padding: 0.2rem 1.6rem 1.3rem 2.1rem; position: relative; }
.st-key-pk-login::before { content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 7px; background: var(--pk-sand); border-radius: 0 0 0 22px; }
.st-key-pk-login [data-testid="stTextInput"] input { background: var(--pk-bg) !important; border-radius: 12px !important; }
.st-key-pk-login [data-testid="stFormSubmitButton"] button { width: 100%; background: var(--pk-tint) !important; color: var(--pk-bg) !important; border: 0 !important; border-radius: 12px !important; font-weight: 700 !important; }
.pk-back { text-align: center; margin-top: 1.1rem; font-size: 0.82rem; }
.pk-back a { color: var(--pk-slate-soft) !important; text-decoration: none; }
.pk-back a:hover { color: var(--pk-tint) !important; }

/* ---------- admin: dashboard ---------- */
.pk-admin-hello { margin: 0.2rem 0 1.2rem; }
.pk-admin-hello .pk-h { font-size: clamp(1.5rem, 4.6vw, 1.9rem); font-weight: 800; letter-spacing: -0.03em; color: var(--pk-text); }
.pk-admin-hello .pk-soft { font-style: italic; font-weight: 400; color: var(--pk-sand); font-variation-settings: "SOFT" 100, "WONK" 1; }
.pk-admin-hello p { color: var(--pk-slate-soft); margin: 0.3rem 0 0; font-size: 0.9rem; }
.pk-stats { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 0.7rem; }
@media (max-width: 640px) { .pk-stats { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
.pk-stat { background: var(--pk-surface); border: 1px solid var(--pk-line); border-radius: 16px; padding: 0.85rem 0.95rem; }
.pk-stat small { display: block; font-size: 0.68rem; letter-spacing: 0.18em; text-transform: uppercase; color: var(--pk-slate); }
.pk-stat strong { display: block; font-size: 1.45rem; font-weight: 800; color: var(--pk-text); letter-spacing: -0.02em; margin: 0.25rem 0 0.1rem; }
.pk-stat span { font-size: 0.75rem; color: var(--pk-slate-soft); word-break: break-word; }
.pk-map { display: grid; grid-template-columns: repeat(auto-fill, minmax(2.6rem, 1fr)); gap: 0.4rem; }
.pk-tile {
  position: relative; aspect-ratio: 3 / 4; border-radius: 6px 10px 10px 6px; border: 1px dashed var(--pk-line);
  display: flex; align-items: flex-end; justify-content: center; padding-bottom: 0.3rem; font-size: 0.72rem; color: var(--pk-slate);
}
.pk-tile.on { border: 1px solid rgba(200, 215, 255, 0.35); color: var(--pk-bg); font-weight: 700; background: rgba(200, 215, 255, var(--pk-fill)); }
.pk-tile.on.light { color: var(--pk-text); }
.pk-tile.on::before { content: ""; position: absolute; left: 3px; top: 3px; bottom: 3px; width: 2px; border-radius: 2px; background: rgba(10, 18, 34, 0.25); }
.pk-tile i { position: absolute; top: 0.3rem; right: 0.35rem; font-style: normal; font-size: 0.6rem; opacity: 0.8; }
.pk-legend { display: flex; flex-wrap: wrap; gap: 1rem; font-size: 0.72rem; color: var(--pk-slate); margin-top: 0.6rem; }
.pk-legend b { display: inline-block; width: 0.8rem; height: 0.8rem; border-radius: 3px; vertical-align: -2px; margin-right: 0.35rem; }
.pk-ver { display: flex; gap: 0.9rem; padding: 0.8rem 0; border-bottom: 1px solid var(--pk-line); }
.pk-ver .dot { flex: none; width: 0.75rem; height: 0.75rem; border-radius: 50%; margin-top: 0.35rem; border: 2px solid var(--pk-slate); }
.pk-ver.active .dot { border-color: #7FD1A8; background: #7FD1A8; box-shadow: 0 0 0 4px rgba(127, 209, 168, 0.15); }
.pk-ver strong { color: var(--pk-text); font-size: 0.92rem; }
.pk-ver span { display: block; font-size: 0.78rem; color: var(--pk-slate-soft); line-height: 1.5; }
.pk-ver em { font-style: normal; font-size: 0.68rem; color: #7FD1A8; border: 1px solid rgba(127, 209, 168, 0.4); border-radius: 99px; padding: 0.05rem 0.5rem; margin-left: 0.4rem; }
.pk-report { background: var(--pk-surface); border: 1px solid var(--pk-line); border-left: 3px solid #7FD1A8; border-radius: 14px; padding: 0.9rem 1rem; font-size: 0.85rem; color: var(--pk-slate-soft); line-height: 1.6; }
.pk-report.fail { border-left-color: var(--pk-sand); }
.pk-report b { color: var(--pk-text); }
.pk-kv { display: grid; grid-template-columns: max-content 1fr; gap: 0.35rem 1.2rem; font-size: 0.85rem; }
.pk-kv dt { color: var(--pk-slate); }
.pk-kv dd { margin: 0; color: var(--pk-text); word-break: break-word; }
[data-testid="stTabs"] button p { font-size: 0.88rem !important; }
@keyframes pk-stamp { from { opacity: 0; transform: rotate(-11deg) scale(1.8); } to { opacity: 1; transform: rotate(-11deg) scale(1); } }

/* ---------- motion ---------- */
@keyframes pk-fade { to { opacity: 1; } }
@keyframes pk-rise { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: none; } }
@keyframes pk-grow { to { max-width: 0.75em; opacity: 1; } }
@keyframes pk-close { to { margin: 0; } }
@keyframes pk-draw { to { stroke-dashoffset: 0; } }
@keyframes pk-cycle { 0% { opacity: 0; transform: translateY(8px); } 3%, 14% { opacity: 1; transform: none; } 17%, 100% { opacity: 0; transform: translateY(-8px); } }
@keyframes pk-drift { from { transform: translateY(20vh); opacity: 0; } 15% { opacity: 1; } 85% { opacity: 1; } to { transform: translateY(-70vh); opacity: 0; } }
@keyframes pk-flip { 0%, 15% { transform: rotateY(0deg); } 60%, 100% { transform: rotateY(-180deg); } }
@keyframes pk-dots { 0% { content: ""; } 25% { content: "."; } 50% { content: ".."; } 75% { content: "..."; } }
@keyframes pk-shimmer { to { background-position: -200% 0; } }
@keyframes pk-breathe { 50% { opacity: 0.45; } }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-delay: 0ms !important; animation-iteration-count: 1 !important; }
}
""".replace("__FONTS__", FONTS)


def _html(text: str) -> str:
    """Strip indentation so Markdown does not turn the HTML into a code block."""
    return "".join(line.strip() for line in text.splitlines())


def style() -> str:
    return f"<style>{CSS}</style>"


def wordmark(size: str = "small") -> str:
    return _html(f"""
        <span class="pk-word pk-word--{size}" role="img" aria-label="pekael">
          <span class="pk-c">p</span><span class="pk-v pk-v1">e</span><span class="pk-c">k</span><span class="pk-v pk-v2">a</span><span class="pk-v pk-v3">e</span><span class="pk-c">l</span>
        </span>""")


def _fact_tick(fact: Fact, index: int) -> str:
    return (
        f'<div class="pk-tick" style="animation-delay:{index * 4}s"><strong>{escape(fact.figure)}</strong>'
        f"<span>{escape(fact.text)}</span><em>hal. {fact.page}</em></div>"
    )


FLOATING_PAGES = ((6, 10, 22), (18, 16, 28), (76, 11, 25), (84, 24, 31), (35, 28, 34), (60, 13, 27))


def intro() -> str:
    floats = "".join(
        f'<span class="pk-float" style="left:{left}%;bottom:-2rem;font-size:{0.9 + (page % 5) * 0.12:.2f}rem;'
        f'animation-duration:{duration}s;animation-delay:{i * 2.3:.1f}s">hal. {page}</span>'
        for i, (left, page, duration) in enumerate(FLOATING_PAGES)
    )
    ticks = "".join(_fact_tick(fact, i) for i, fact in enumerate(FACTS))
    lines = "".join(f"<p>{escape(line)}</p>" for line in INTRO_LINES)
    return _html(f"""
        <section class="pk-intro">
          {floats}
          <div class="pk-kicker">PKL · PTIK · UNJ</div>
          {wordmark("hero")}
          <svg class="pk-stroke" viewBox="0 0 320 26" aria-hidden="true"><path d="M6 16 C 60 4, 110 24, 160 13 S 262 5, 314 15"/></svg>
          <div class="pk-spoken">PKL, kalau dibaca jadi <b>pe·ka·el</b></div>
          <div class="pk-lines">{lines}</div>
          <div class="pk-ticker" aria-label="Tahukah kamu">{ticks}</div>
        </section>""")


def top_bar(source_label: str, ready: bool) -> str:
    state = "" if ready else " pk-off"
    return _html(f"""
        <div class="pk-top pk-enter">{wordmark()}
          <span class="pk-pill{state}"><i></i>{escape(source_label)}</span>
        </div>""")


def greeting(title: str, sub: str) -> str:
    head, _, tail = title.partition(",")
    return _html(f"""
        <div class="pk-hello pk-enter"><div class="pk-h">{escape(head)},<span class="pk-soft">{escape(tail)}</span></div><p>{escape(sub)}</p></div>""")


def label(text: str) -> str:
    return f'<div class="pk-label">{escape(text)}</div>'


def facts_grid() -> str:
    cards = "".join(
        f'<div class="pk-fact"><strong>{escape(f.figure)}</strong><span>{escape(f.text)}</span><em>hal. {f.page}</em></div>'
        for f in FACTS
    )
    return f'<div class="pk-facts pk-enter">{cards}</div>'


def question_bubble(question: str, time: str = "") -> str:
    stamp = f'<span class="pk-time">{escape(time)}</span>' if time else ""
    return f'<div class="pk-q"><div>{escape(question)}</div>{stamp}</div>'


def time_stamp(time: str) -> str:
    return f'<div class="pk-time">{escape(time)}</div>'


def page_tabs(pages: list[int], document: str) -> str:
    tabs = "".join(f'<span class="pk-page">hal. {p}</span>' for p in pages)
    return f'<div class="pk-pages"><small>{escape(document)}</small>{tabs}</div>'


def quote(page: int, section: str | None, snippet: str | None) -> str:
    heading = f"Halaman PDF {page}" + (f" · {section}" if section else "")
    return f'<div class="pk-quote"><b>{escape(heading)}</b><span>{escape(snippet or "")}</span></div>'


def loading(text: str, step: int = 0, total: int = 0, hint: str = "") -> str:
    bars = "".join(
        f'<u class="{"on" if i < step else "now" if i == step else ""}"></u>' for i in range(total)
    )
    steps = f'<div class="pk-steps">{bars}</div>' if total else ""
    hint_html = f"<span>{escape(hint)}</span>" if hint else ""
    return _html(f"""
        <div class="pk-loading"><div class="pk-book"><i></i></div>
          <div class="pk-loading-text"><b class="pk-dots">{escape(text)}</b>{hint_html}{steps}</div>
        </div>""")


def boot() -> str:
    return _html(f"""<div class="pk-boot">{wordmark()}<div class="pk-dots">Menyiapkan buku pedoman</div></div>""")


# ---------- admin ----------

def login_card(card_number: str) -> str:
    return _html(f"""
        <div class="pk-card-wrap"><div class="pk-card">
          <div class="pk-card-kicker">Kartu pengelola · Pekael</div>
          <div class="pk-card-title">{wordmark()}<em>ruang admin</em></div>
          <div class="pk-card-sub">Khusus pengelola buku pedoman. Masuk untuk mengganti buku, melihat versi, dan menguji jawaban.</div>
          <div class="pk-card-row"><span>NO. {escape(card_number)}</span><span>PTIK · UNJ</span></div>
          <div class="pk-stamp">RUANG ADMIN</div>
        </div></div>""")


def admin_hello(name: str) -> str:
    return _html(f"""
        <div class="pk-admin-hello pk-enter"><div class="pk-h">Halo, <span class="pk-soft">{escape(name)}</span>.</div>
        <p>Semua perubahan di sini langsung dipakai mahasiswa.</p></div>""")


def stats(items: list[tuple[str, str, str]]) -> str:
    cards = "".join(
        f'<div class="pk-stat"><small>{escape(label)}</small><strong>{escape(value)}</strong><span>{escape(note)}</span></div>'
        for label, value, note in items
    )
    return f'<div class="pk-stats pk-enter">{cards}</div>'


def page_map(total_pages: int, chunks_per_page: dict[int, int]) -> str:
    """One tile per PDF page: lit and brighter with more chunks, dashed when not in the knowledge base."""
    most = max(chunks_per_page.values(), default=1)
    tiles = []
    for page in range(1, max(total_pages, max(chunks_per_page, default=0)) + 1):
        count = chunks_per_page.get(page, 0)
        if count:
            fill = 0.25 + 0.65 * count / most
            light = " light" if fill < 0.5 else ""
            tiles.append(f'<div class="pk-tile on{light}" style="--pk-fill:{fill:.2f}" title="Halaman {page}: {count} potongan">'
                         f'<i>{count}</i>{page}</div>')
        else:
            tiles.append(f'<div class="pk-tile" title="Halaman {page}: tidak dipakai">{page}</div>')
    legend = ('<div class="pk-legend"><span><b style="background:rgba(200,215,255,.9)"></b>dipakai, makin terang makin banyak potongan</span>'
              '<span><b style="border:1px dashed #22324F"></b>tidak dipakai</span><span>angka kecil = jumlah potongan</span></div>')
    return f'<div class="pk-map">{"".join(tiles)}</div>{legend}'


def version_row(title: str, detail: str, active: bool) -> str:
    badge = "<em>aktif</em>" if active else ""
    css = "pk-ver active" if active else "pk-ver"
    return f'<div class="{css}"><div class="dot"></div><div><strong>{escape(title)}</strong>{badge}<span>{escape(detail)}</span></div></div>'


def report_box(lines: list[str], failed: bool = False) -> str:
    body = "<br>".join(lines)  # lines are built from escaped values by the caller
    return f'<div class="pk-report{" fail" if failed else ""}">{body}</div>'


def key_values(rows: list[tuple[str, str]]) -> str:
    items = "".join(f"<dt>{escape(k)}</dt><dd>{escape(v)}</dd>" for k, v in rows)
    return f'<dl class="pk-kv">{items}</dl>'
