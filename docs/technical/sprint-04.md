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

## Sesi 4 — 16 November 2026

**Simpanan jawaban (D-41)** — `ChatbotManager`
- `normalise_question()` (lower, spasi tunggal, buang `?!.,` di akhir). Kunci `(pertanyaan, manifest.build_id)`, `OrderedDict` LRU `cache_size=256`, `threading.Lock`. Disimpan hanya `answered`/`out_of_scope`. `clear_cache()` dipanggil setelah `initialize_knowledge_base` berhasil dan saat versi diaktifkan. `cached_answers()` untuk ruang admin.

**Dukungan admin**
- `BaseLoader.load(source_path, *, pages=None, on_page=None)`, `PDFLoader` melaporkan `on_page(done, total)`.
- `ChatbotManager.initialize_knowledge_base(source_path, pages=None, on_progress=None)`: tahap `BUILD_STAGES = ("load", "split", "index")`, `build_info["source_path"]` dan `knowledge_base_pages` dicatat di manifest.
- `FaissVectorStore`: manifest baru memuat `chunks_per_page` dan `total_pages`, `versions()` (terbaru dulu, `active`), `activate_version(build_id)` (cek manifest, model embedding, muat folder, lalu ganti `ACTIVE`), `chunks_per_page()` dan `total_pages()` (cadangan dari docstore untuk build lama).

**Tampilan**
- `app.py`: `st.navigation([...], position="hidden")`, halaman mahasiswa `/` dan ruang admin `/admin`. `set_page_config` pindah ke `app.py`.
- `student_page.py`: `Exchange.asked_at`/`answered_at`, jam di bawah gelembung, kartu jawaban `width: fit-content`, `max-width: min(86%, 38rem)` (kiri), pertanyaan `max-width: min(78%, 34rem)` (kanan), tautan kecil "Masuk ruang admin".
- `src/pekael/ui/admin_page.py`: login (`AdminAuthenticator`, `hmac.compare_digest`, 5 kali salah → kunci 30 s per sesi), dashboard (statistik, peta halaman, tab Ganti buku pedoman / Riwayat versi / Uji pertanyaan / Pengaturan). Unggahan: cek `%PDF-` dan `PDF_MAX_UPLOAD_MB`, nama file dibersihkan, disimpan di `data/source/uploads/` (di-ignore), dihapus bila pembangunan gagal. Tesseract dicek sebelum membangun.
- `.streamlit/config.toml`: `server.maxUploadSize = 30`.
- Akun admin: `.env` `ADMIN_USERNAME`, `ADMIN_PASSWORD` diisi dengan skrip yang hanya mengganti dua baris tersebut (D-42). Kata sandi tidak ditemukan di file mana pun di luar `.env` (`grep -rl`).

**Uji**
- `tests/unit/test_admin_core.py` (14): simpanan jawaban, normalisasi, ukuran simpanan, build baru, kemajuan dan pilihan halaman, `PDFLoader` pilihan halaman, versi dan rollback, model berbeda ditolak, statistik halaman build lama.
- `tests/unit/test_admin_page.py` (14, `tests/fixtures/admin_app.py`): kartu login, kata sandi salah, login benar, kunci setelah 5 kali, akun belum diatur, keluar, tombol bangun, bangun ulang dan laporan, bangun gagal, format halaman salah, aktifkan versi, uji pertanyaan, pengaturan tanpa secret, validasi unggahan.
- Website (Edge headless + CDP, kredensial dibaca dari konfigurasi): "Berapa lama PKL dilaksanakan?" 6,1 s, "Apa itu machine learning?" 2,0 s, pertanyaan pertama diulang 1,0 s (simpanan). Temuan yang diperbaiki: formulir login tidak menyatu dengan kartu (kelas key tidak melekat pada `st.form`, dibungkus `st.container(key=...)`), nama admin belum memakai huruf aksen, batas unggahan tampil 200 MB.
- `pytest` → **268 lulus, 0 gagal**.

**Login admin ditolak (laporan Developer)**: log `Admin sign-in failed`. Diperiksa tanpa mencetak nilai: satu baris `ADMIN_USERNAME` dan `ADMIN_PASSWORD` di `.env`, tidak ada `ADMIN_*` di environment Windows, `verify("admin1", <kata sandi yang diminta>)` = `True`, dengan spasi di akhir atau `Admin1` = `False`. `AdminAuthenticator` kini `strip()` kedua nilai dan `casefold()` nama pengguna, kata sandi tetap peka huruf besar-kecil. Test baru `test_case_of_username_and_surrounding_spaces_are_ignored` (3 kasus). `pytest` → **271 lulus, 0 gagal**.

**Login masih ditolak (laporan Developer)**: AppTest dengan `.env` asli (tanpa tiruan) → `Admin signed in`. Server baru di port 8501, Edge headless mengetik dengan CDP `Input.insertText` → dashboard terbuka, log `Admin signed in`. Dugaan: isian otomatis browser (`autocomplete="username"`/`current-password`) tampil tetapi tidak terkirim ke Streamlit. Diubah ke `autocomplete="off"` dan `"new-password"`, isian kosong memberi peringatan dan tidak menambah hitungan gagal. Test baru: `test_empty_fields_ask_to_type_and_do_not_count_as_failure`, `test_autofill_is_turned_off`. `pytest` → **273 lulus, 0 gagal**.

**Login masih ditolak (laporan kedua)**: dugaan variabel lingkungan `ADMIN_*` di terminal Developer (misalnya dimuat VS Code saat terminal dibuka) yang mengalahkan `.env`. Ditambahkan `AppConfigurator.overridden_settings()` dan peringatan log berisi nama pengaturan saja (`ADMIN_USERNAME`, `ADMIN_PASSWORD`, `GEMINI_API_KEY`, `GEMINI_CHAT_MODEL`), log gagal login menyebut apakah nama pengguna cocok, dan `scripts/check_admin_login.py` (asal nilai, kecocokan nama pengguna dan kata sandi, panjang kata sandi, tanpa mencetak kata sandi). Test baru `test_environment_override_of_admin_settings_is_reported_by_name`. `pytest` → **274 lulus, 0 gagal**.

**Tanggal versi mengikuti linimasa sprint** (permintaan Developer): `created_at` di `manifest.json` diubah, nilai asli disimpan di `created_at_original`. Build `20261104T043244948591-565a9929` (aktif): `2026-11-04T04:32:47+00:00` → `2026-11-15T04:32:47+00:00`. Build `20261102T180419398924-565a9929`: `2026-11-02T18:04:21+00:00` → `2026-11-07T18:04:21+00:00`, yaitu 8 November 2026 01.04 WIB (tanggal pembangunan pertama menurut logbook Sprint 3). Tanggal di panel samping mahasiswa kini memakai waktu lokal seperti ruang admin. `build_id` tetap memuat waktu asli. Tanggal kalender hari ini dihapus dari sapaan ruang admin. Build baru dari ruang admin tetap memakai waktu saat dibangun.

## Sesi 5 — 17 November 2026

**Jadwal (D-44)**: Sprint 4–6 masing-masing 1 minggu. Diperbarui: `docs/scrum/README.md`, `sprint-04/sprint_planning.md` (periode, waktu tugas, tugas 9, jadwal review/retro 19 Nov), `sprint-04/sprint_backlog.md`, `product_backlog.md`, `decision_log.md`.

**Respons arahan (S4-T09, D-45)** — `src/pekael/core/prompts.py`
- Aturan prompt no. 5: `TIDAK_DITEMUKAN` di baris pertama, lalu 2–3 kalimat arahan (sapaan "kamu", tanpa menebak, tanpa menyatakan informasi tidak ada, boleh menyebut informasi terkait dari konteks, satu pihak yang sesuai: Koordinator PKL, Admin Prodi PTIK, Koordinator Program Studi/Kaprodi, tanpa tanggal, nama, kontak, atau aturan di luar konteks). Aturan no. 7: `SUMBER: -` bila tidak ada konteks yang dipakai.
- `ParsedAnswer.redirect`, `parse_answer` mengenali penanda di baris pertama dan menyimpan sisa teks serta nomor `SUMBER`.
- `REDIRECT_MESSAGES` (4) dan `OFF_TOPIC_MESSAGES` (4), `pick_message(question, options)` memilih berdasarkan `crc32` pertanyaan yang dinormalisasi, sehingga stabil per pertanyaan. `FALLBACK_MESSAGE = REDIRECT_MESSAGES[0]` (menggantikan teks fallback spec §4.4 atas permintaan PO).
- `DISCOURAGED_PHRASES` dan `usable_redirect()` (tidak kosong, ≤ 700 karakter, tanpa ungkapan terlarang).
- `rag_steps.py`: hasil pencarian kosong dan penolakan ambang memakai `OFF_TOPIC_MESSAGES`. `validate_citations` memakai arahan model bila `usable_redirect`, bila tidak `REDIRECT_MESSAGES`, rujukan dari nomor `SUMBER` arahan. Status tetap `out_of_scope` sehingga simpanan jawaban dan evaluasi tidak berubah.
- `student_page.py`: label "Saran dari Pekael", arahan ditampilkan sebagai teks biasa beserta penanda halaman bila ada.

**Uji langsung** (`scripts/ask.py`, `gemini-3.5-flash-lite`)
- Putaran 1 (11 pertanyaan): L1 "...tidak tersedia pada panduan ini...", L4 "...belum tercantum di dalam pedoman...", beberapa arahan menyalin daftar peran dari prompt, sapaan "Anda" dan "kamu" bercampur. N1–N3 memakai kalimat siap pakai (0,41–0,52 s). Pertanyaan dalam cakupan tidak berubah (100 SKS hal. 10, nilai 74 hal. 16 dan 11). No. 22 tetap diarahkan, tidak dijawab.
- Perbaikan: `DISCOURAGED_PHRASES` ditambah `tidak tersedia`, `tidak tercantum`, `belum tercantum`, `tidak terdapat`, `tidak ada di`, `tidak dijelaskan`. Prompt: sapaan "kamu", tidak menyatakan informasi tidak ada, pilih satu pihak tanpa menyalin daftar.
- Putaran 2 (7 pertanyaan): 5 arahan tanpa ungkapan terlarang, sapaan "kamu", pihak berbeda sesuai topik (pendaftaran, lowongan, nama koordinator, format laporan → Admin Prodi PTIK, kerja paruh waktu → Koordinator PKL), 1,52–2,85 s. Pertanyaan dalam cakupan: lama PKL hal. 14 dan 7, dokumen lampiran hal. 24.

**Test**: `test_prompts.py` (pesan siap pakai, kontak di prompt, pilihan pesan stabil dan bervariasi, ungkapan terlarang, arahan kosong atau terlalu panjang, arahan model dan rujukannya), `test_rag_steps.py` (arahan model dipakai, ungkapan terlarang diganti, ambang memakai pesan di luar topik), `test_student_page.py` (label). `pytest` → **296 lulus, 0 gagal**.

## Sesi 6 — 18 November 2026

**Waktu persiapan (masukan Developer: jawaban cepat tetapi menunggu lama sebelum muncul, juga dari intro ke halaman tanya-jawab)**

Pengukuran awal (`cold_start.py` sementara, proses baru):

| Tahap | Waktu |
|---|---|
| `import langchain_core` | 0,85 s |
| `import langchain_google_genai` | 6,00 s |
| `import faiss` + `langchain_community` | 2,09 s |
| `import pekael` (sisa) | 6,66 s |
| `create_manager_from_config` | 4,10 s |
| Muat indeks FAISS | 0,07 s |
| Embedding #1 / #2 | 0,49 s / 0,36 s |
| Gemini #1 / #2 (prompt pendek) | 3,51 s / 0,74 s |

`python -X importtime`: `pymupdf` 2,25 s (termasuk `pymupdf.layout`), `pytesseract` 1,07 s yang memuat `pandas` 1,06 s. Keduanya hanya dipakai saat membangun knowledge base.

**Perbaikan**
- Impor malas: `pdf_loader.py` (PyMuPDF, Pillow saat PDF dibuka), `ocr_service.py` (`pytesseract` saat OCR dipakai, path Tesseract diterapkan di `_pytesseract()`), `faiss_vector_store.py` (`langchain_community.vectorstores.FAISS` saat indeks dibangun atau dimuat). `from __future__ import annotations` dan `TYPE_CHECKING` untuk anotasi.
- `ChatbotManager.warm_up()`: muat indeks, satu embedding (`"PKL"`), satu permintaan Gemini pendek. Kegagalan dicatat, tidak dilempar.
- `student_page.start_warm_up()`: thread latar belakang sekali per proses saat halaman pertama (intro) dibuka. `_build_manager()` dengan `threading.Lock` agar manager hanya dibuat sekali walau thread dan halaman memintanya bersamaan.
- `scripts/ask.py` mode interaktif: `warm_up()` berjalan di thread selama pertanyaan pertama diketik.

**Sesudah perbaikan** (proses baru, tanpa panggilan API): `import pekael` 2,05 s, `create_manager_from_config` 5,03 s (memuat `langchain_google_genai`), muat indeks 0,08 s, total 7,16 s. `pymupdf`, `pytesseract`, `pandas` tidak dimuat. Di website, tahap ini berjalan selama intro.

**Test**: `test_warm_up_loads_index_and_opens_both_connections`, `test_warm_up_failure_is_not_raised`. Fixture `test_student_page.py` mengganti `start_warm_up` agar tidak ada thread di test.

**Gaya bahasa adaptif (D-46)** — `src/pekael/core/prompts.py`
- `STYLE_RULES` dipakai `SYSTEM_PROMPT` dan `CONVERSATION_PROMPT`: ikuti gaya pertanyaan, parafrase kecuali angka, nilai, tanggal, nama dokumen, istilah resmi, isi daftar, kalimat penenang hanya bila mahasiswa menyatakan cemas, tidak membuka dengan "Halo"/"Hai" kecuali disapa, tidak memanggil mahasiswa "kak". Contoh kalimat dihapus dari prompt setelah Gemini menyalin contoh "Bisa kok, asal SKS-mu sudah 100." mentah-mentah.
- `detect_register()` (`CASUAL_WORDS`, `FORMAL_WORDS`), `register_line()` disisipkan ke prompt pengguna sebagai `GAYA BAHASA PERTANYAAN: santai|formal|netral`. `strip_unasked_greeting()` membuang "Halo!"/"Hai!" di awal bila pertanyaan tidak menyapa.
- `RagSteps.conversation_reply()`: pertanyaan yang ditolak ambang atau tanpa hasil pencarian dijawab Gemini dengan `CONVERSATION_PROMPT` dan `build_conversation_prompt()` (tanpa konteks buku). `usable_conversation()` menolak balasan berisi angka, ungkapan terlarang, atau penanda. Kegagalan apa pun → `OFF_TOPIC_MESSAGES`.
- `is_marker()`: penanda dikenali walau salah eja (`TIDAK_DITEMUCHAP` muncul pada uji langsung). `is_unmarked_redirect()`: jawaban yang menyatakan informasi tidak ada di panduan dan menyebut Admin Prodi/Koordinator PKL/Kaprodi diperlakukan sebagai arahan (muncul pada uji langsung untuk batas pendaftaran).
- `student_page.py`: label "Saran dari Pekael" dihapus, balasan percakapan dan arahan tampil sebagai teks biasa.

**Ambang hanya memutuskan (D-47)**: `relevancy_gate` menolak bila jarak terdekat > `RETRIEVAL_MAX_L2_DISTANCE`, bila lolos keempat potongan dipakai. Pemeriksaan pencarian `"kak, kalo nilai aku 74 lulus gak?"`: hal. 16 (0,617), hal. 28 (0,652), hal. 11 `011-c02` berisi syarat B+ (0,661), hal. 27 (0,682). Sebelumnya hanya hal. 16 yang lolos dan Gemini menjawab "statusnya lulus kok!". Sesudah perbaikan prompt, jawabannya membandingkan ke syarat B+ dan menyimpulkan belum lulus.

**Uji langsung gaya** (`scripts/ask.py`, tiga putaran): putaran terakhir, formal "Bagaimana prosedur pengajuan PKL bagi mahasiswa PTIK?" → bahasa baku, "Anda", "Apakah mahasiswa dengan 90 SKS …" → "Karena jumlah SKS Anda baru mencapai 90 SKS, maka Anda belum memenuhi syarat minimal 100 SKS", santai "kak dokumen apa aja sih …" → "dokumen yang harus kamu lampirin … ada beberapa macam, nih", "halo kak" → "Halo juga! Ada yang bisa aku bantu …".

**EXP-007**: lihat `experiment_log.md`. Data mentah `data/processed/Pedoman-PKL-2025/exp007.json`.

**Pengukuran waktu di website**: tidak dijalankan pada sesi ini. Langkah yang menghentikan semua proses Streamlit di komputer Developer ditolak oleh pengaman otomatis.

**Test**: `pytest` → **315 lulus, 0 gagal** (baru: deteksi gaya, sapaan pembuka, balasan percakapan dan penggantinya, penanda salah eja, arahan tanpa penanda, ambang mempertahankan semua potongan, Tesseract malas).

## Sesi 7 — 19 November 2026

**Variasi penyajian (D-49)** — `src/pekael/core/prompts.py`
- `ANSWER_FORMS` (5), `REDIRECT_FORMS` (4), `CONVERSATION_FORMS` (3). `presentation_lines(rng)` memilih acak satu bentuk jawaban dan satu bentuk arahan, disisipkan ke prompt pengguna (`BENTUK PENYAJIAN`, `BENTUK ARAHAN`, "Isi daftar tetap lengkap"). `build_conversation_prompt` menyisipkan `BENTUK BALASAN`. `STYLE_RULES` no. 5: ringkas, sekitar 2–4 kalimat di luar daftar.
- `REDIRECT_MESSAGES` dan `OFF_TOPIC_MESSAGES` masing-masing 6.
- Simpanan jawaban tetap berlaku: pertanyaan yang sama persis mendapat jawaban yang sama.

**EXP-008 (waktu jawab)**: skrip sementara (dihapus), 6 pertanyaan × 2 putaran, prompt dan konteks yang sama, koneksi dipanaskan lebih dulu. `reasoning_effort` bawaan median 8,03 s (maks 11,00 s), `minimal` median 8,65 s (maks 14,59 s). `SYSTEM_PROMPT` commit `a9616d0` (933 karakter) median 7,21 s (n=11, satu `LLMError`), `SYSTEM_PROMPT` sekarang (3.335 karakter) median 7,04 s.

**Uji langsung** (`scripts/ask.py`, 8 pertanyaan): 5,30–8,72 s. "apa itu pkl?" → definisi lalu daftar 2 poin, "Apakah pengertian dari Praktik Kerja Lapangan di dalam Prodi PTIK?" → paragraf baku dengan "Anda", "kak pkl itu apaan sih?" → "Jadi gini ya, … Intinya, …". Arahan: batas pendaftaran → mengakui pertanyaan lalu Admin Prodi PTIK, jadwal pembekalan → langsung Admin Prodi PTIK, izin PKL di luar kota → Koordinator PKL dengan alasan.

**Test**: `test_every_prompt_carries_one_presentation_form_picked_at_random`, `test_ready_made_messages_have_more_variants`. `pytest` → **317 lulus, 0 gagal**.

**Pertanyaan tidak terjawab (laporan Developer)**: reproduksi `scripts/ask.py`: "kak dokumen apa aja yg dilampirin di laporan?" → `TIDAK_DITEMUCH TAPI TANYA ADMIN PRODI PTIK YAA…` dengan status `answered`, "apa itu pkl?" → dibuka "Hai, kamu mau tahu tentang PKL ya?".

**Perbaikan (D-50)**
- `presentation_lines()` hanya `BENTUK PENYAJIAN`. `system_prompt_with_redirect_form()` menambahkan catatan bentuk arahan di akhir instruksi sistem, dipanggil di `RagSteps.generate`.
- `split_marker()` dengan `_MARKER_PREFIX` (`^\W*TIDAK[\s_]*DITEMU[A-Z]*\W*`), sisa teks setelah penanda menjadi arahan. `_shouting()` menolak arahan serba kapital. `_LEADING_GREETING` juga menerima `?`. `DISCOURAGED_PHRASES` ditambah `belum ada di`, `belum tersedia`.
- Test baru: penanda diikuti teks pada baris yang sama (3 kasus), jawaban diawali "Tidak," bukan penanda, arahan serba kapital, catatan bentuk arahan di instruksi sistem, kalimat sapaan bertanda tanya.

**EXP-009**: lihat `experiment_log.md`, data `data/processed/Pedoman-PKL-2025/exp009.json`.

**Format tanda tangan (D-51)**: `scripts/export_docs.py` `PERSONAL_PLACEHOLDERS` ditambah `NIP_SCRUM_MASTER_REVIEW`, `NIP_SCRUM_MASTER_RETRO`, `.env.example` diperbarui, templat `sprint_review.md` (Nur Elah) dan `sprint_retrospective.md` (Dr. Widodo) diubah.

**Test**: `pytest` → **327 lulus, 0 gagal**.

**Daftar pertanyaan uji**: `docs/scrum/sprint-04/pertanyaan_uji.md` dibuat dari `topik_pertanyaan.md` (no. 1–30) dan `EXTRA_IN_SCOPE` (E1–E6), kolom hasil dari `exp009.json`. `export_docs.py` mendapat judul untuk `pertanyaan_uji`. Salinan ekspor `docs/export/sprint-04/pertanyaan_uji_4_DeniM.docx` dan `.pdf` (di-ignore git).
