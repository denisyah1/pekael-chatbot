# Log Teknis Sprint 4

> Ringkasan berbahasa sederhana: [`docs/scrum/sprint-04/`](../scrum/sprint-04/sprint_backlog.md)

## Sesi 1 — 13 November 2026

**Halaman mahasiswa (S4-T02, S4-T03)**
- `app.py` (entry point, spec §5.4) memanggil `pekael.ui.student_page.main()`.
- `src/pekael/ui/student_page.py`:
  - `get_config()` dan `get_manager()` memakai `st.cache_resource`, sehingga satu `ChatbotManager` dan satu indeks FAISS dipakai bersama oleh semua sesi pada satu proses server.
  - `load_manager()` → `(manager, None)`, atau pesan `NOT_CONFIGURED` (`ConfigError`/`EmbeddingError`/`LLMError` saat perakitan, misalnya `GEMINI_API_KEY` kosong), atau `NOT_READY` (`IndexNotReadyError`). Indeks dimuat sekali (`is_ready`).
  - `st.form(clear_on_submit=True)`: `st.text_area` (`max_chars=QUESTION_MAX_CHARS`) dan tombol "Kirim". `st.spinner` selama `generate_response`.
  - Riwayat `st.session_state["history"]` berisi `Exchange(question, response)`, terbaru di atas, hanya untuk tampilan (FR-10). `INVALID_INPUT` tidak disimpan.
  - Status: `answered` → jawaban + `st.caption("Sumber: <dokumen>, halaman PDF ...")` + `st.expander` cuplikan per potongan. `out_of_scope` → `st.info`. `unavailable`/`error` → `st.warning`.
- `.streamlit/config.toml`: tema terang, `primaryColor="#1F6F43"`, `toolbarMode="minimal"`, `gatherUsageStats=false`. `.streamlit/secrets.toml` tetap di-ignore.
- README: bagian "Menjalankan Pekael".

**Uji**
- `tests/unit/test_student_page.py` (9 test, `streamlit.testing.v1.AppTest` dengan manager tiruan): tampilan awal, jawaban + sumber + kutipan, penolakan, gangguan layanan, pertanyaan kosong, urutan riwayat dan hapus riwayat, knowledge base belum ada, pengaturan belum lengkap.
- `streamlit run app.py --server.headless true --server.port 8599` → `/_stcore/health` = `ok`, halaman HTTP 200.
- AppTest dengan manager asli (indeks `20261104T043244948591-565a9929`): "Kalau nilai saya 74, apakah saya lulus PKL?" → `answered`, 3 rujukan (hal. 16, 11, 11), 19,70 s (pertanyaan pertama setelah start). "Bagaimana cara membuat nasi goreng?" → `out_of_scope` oleh ambang (jarak 0,831), 0,47 s. Tidak ada exception.
- `pytest` → **233 lulus, 0 gagal**.

## Sesi 2 — 14 November 2026

**Rancangan ulang tampilan (S4-T04, D-38)**
- `src/pekael/ui/content.py`: teks, `FACTS` (6 fakta dengan halaman, dicek ke `data/processed/.../page_0NN.txt`: 100 SKS hal. 10, 4 bulan hal. 14, B+ hal. 11, 6 SKS hal. 13, 30/40/30 hal. 28, 8 dokumen hal. 24), `EXAMPLES`, `STEP_LABELS`.
- `src/pekael/ui/theme.py`: CSS (token warna `--pk-bg #0A1222`, `--pk-surface #111C31`, `--pk-slate #7D90AE`, `--pk-tint #C8D7FF`, `--pk-sand #F1D9B8`), font dari Google Fonts (`Plus Jakarta Sans` 400–800, `Fraunces` italic dengan sumbu `SOFT`/`WONK`), wordmark `p·e·k·a·e·l` (konsonan sans 800, vokal serif miring), intro dengan animasi CSS (`pk-grow`, `pk-close`, `pk-draw`, `pk-cycle`, `pk-drift`), `prefers-reduced-motion` dihormati. Tanpa JavaScript, teks pengguna di-`escape`.
- `.streamlit/config.toml`: `base="dark"`, warna sesuai token.
- `student_page.py`: alur intro (`session_state["intro_done"]`, intro dalam `st.empty()` lalu dikosongkan saat klik agar tidak tertinggal) → layar `boot` saat `load_manager()` pertama → halaman utama. `st.chat_input(submit_mode="disable")`, contoh pertanyaan `st.button(key="pk-ex-N")`, kartu jawaban `st.container(key="pk-a-N")`, sidebar dari `manifest.json` (halaman, jumlah potongan, tanggal build).

**Tanda proses dari LangChain callback**
- `Chain.invoke(input_data, config=None)` meneruskan `RunnableConfig`.
- `ChatbotManager.generate_response(message, on_step=None)`: `_StepReporter(BaseCallbackHandler).on_chain_start` memanggil `on_step(nama_langkah)` untuk langkah yang benar-benar berjalan (input `ChainState` tanpa `response`). Callback dijalankan di thread utama (diperiksa: `MainThread`), sehingga placeholder Streamlit dapat diperbarui langsung.

**Pesan**: `core/messages.py` tanpa istilah "AI" (`QUOTA_EXHAUSTED`, `SERVICE_UNAVAILABLE`, `SERVICE_MISCONFIGURED`, `INDEX_NOT_READY`, `RETRIEVAL_FAILED`).

**Uji**
- `tests/unit/test_student_page.py` ditulis ulang (12 test): intro dan tombol mulai, sapaan/contoh/fakta/sumber, jawaban dengan gelembung + penanda halaman + kutipan + progres, tombol contoh, escape teks, label penolakan dan gangguan, pertanyaan kosong (toast), urutan riwayat dan percakapan baru, knowledge base belum ada, pengaturan belum lengkap, fungsi format, fakta dan nama langkah.
- `tests/unit/test_chatbot_manager.py`: `test_progress_reports_only_steps_that_run`.
- Tangkapan layar: Edge headless dikendalikan lewat Chrome DevTools Protocol (skrip sementara di luar repo, pustaka `websockets` yang sudah terpasang), ukuran 1280 px dan 390 px. Temuan yang diperbaiki: judul sapaan seluruhnya serif karena Streamlit membungkus isi `h2` dengan `span` (diganti `div.pk-h`), teks tombol contoh terpotong (`white-space: normal`), tombol mulai melebar penuh, tombol intro tertinggal saat layar persiapan.
- `pytest` → **237 lulus, 0 gagal**.

## Sesi 3 — 15 November 2026

**Gejala**: log `ERROR pekael.core.rag_steps: Generation failed (unavailable)` lalu `Answered with status=unavailable sources=0 nearest=- in 62.00 s`.

**Diagnosis** (skrip sementara, `ChatGoogleGenerativeAI` langsung, `timeout=45`, `max_retries=0`, prompt "Jawab satu kata: ibu kota Indonesia?", teks galat disaring dari secret):

| Model | Hasil |
|---|---|
| `gemini-3.5-flash-lite` | 27,96 s, `504 DEADLINE_EXCEEDED` setelah 44,15 s, 15,39 s, 29,63 s (prompt sistem + konteks), lalu 10,72 s dan 19,04 s |
| `gemini-3.5-flash` | 5,30 s dan 3,45 s |
| `gemini-2.5-flash-lite`, `gemini-2.5-flash` | `404 NOT_FOUND`, tidak tersedia untuk pengguna baru |

62 s = `timeout` 30 s + jeda 2 s + percobaan ulang 30 s, karena timeout digolongkan `unavailable` yang dicoba ulang.

**Perbaikan (D-39)**
- `gemini_model.py`: `is_timeout()` (`504`, `DEADLINE_EXCEEDED`, `timed out`, `Timeout`). Percobaan ulang hanya untuk `unavailable` yang bukan timeout. `504` ditambahkan ke penanda `unavailable`.
- `settings.py`: `gemini_timeout_seconds` (`GEMINI_TIMEOUT_SECONDS`, bawaan 30, 0 < nilai ≤ 120), diteruskan `create_manager_from_config` ke `GeminiModel(timeout=...)`. `.env.example` diperbarui.
- `ui/content.py`: `SLOW_HINT` ditampilkan pada langkah `generate`.

**Test**: `test_timeout_is_not_retried` (2 kasus), `test_gemini_timeout_is_configurable_and_bounded`. `pytest` → **240 lulus, 0 gagal**.

**EXP-005** (`gemini-3.5-flash`): `.env` `GEMINI_CHAT_MODEL` diganti dengan skrip satu baris, `run_threshold_experiment.py` mendapat opsi `--output` agar `exp004.json` tidak tertimpa. Hasil: 13/36 dijawab, lalu `429 RESOURCE_EXHAUSTED` (`GenerateRequestsPerDayPerProjectPerModel-FreeTier`, `quotaValue` 20, `retryDelay` 56325 s). `.env` dikembalikan ke `gemini-3.5-flash-lite` (D-40).

**Waktu per langkah** (callback `on_step`, `gemini-3.5-flash-lite`, 3 pertanyaan): `retrieve` 0,48–0,56 s, `generate` 22,75–28,79 s (satu `unavailable`), langkah lain < 0,01 s, muat indeks 0,05 s. Streaming satu prompt alur lengkap (4.556 karakter): token pertama 13,91 s, selesai 14,07 s, 6 potongan. Waktu tunggu terjadi sebelum token pertama, sehingga streaming tidak mempersingkat waktu tunggu. Batas tier gratis menurut Developer: 15 permintaan per menit, 500 per hari.
