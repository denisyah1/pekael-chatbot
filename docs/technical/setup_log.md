# Log Teknis Fase Setup

> Rincian teknis fase Setup: perintah, versi, hasil test, dan file yang berubah.
> Ringkasan dengan bahasa sederhana ada di [`docs/scrum/setup_phase.md`](../scrum/setup_phase.md).

## Sesi 1 — 2026-10-23

**Dikerjakan**
- Spec dibaca dan dianalisis, `implementation_plan.md` disusun dan dinyatakan lengkap oleh pemilik proyek.
- `.gitignore` diisi: secret, data penelitian, PDF, dan file bantu Claude Code dikecualikan karena repo bersifat public.
- Python **3.11.9** dipasang via `winget` (scope user) di `C:\Users\dwiki\AppData\Local\Programs\Python\Python311\python.exe`. Python 3.13 tetap ada tetapi tidak dipakai untuk proyek ini.
- Tesseract OCR **5.4.0.20240606** (build UB Mannheim) dipasang via `winget` di `C:\Program Files\Tesseract-OCR\`.
- Data bahasa `ind.traineddata` (8.279.230 byte) diunduh dari `github.com/tesseract-ocr/tessdata` (branch `main`) dan disalin ke folder `tessdata`. Hasil `tesseract --list-langs`: `eng`, `ind`, `osd`.
- Struktur dokumentasi Scrum dibuat di `docs/scrum/`.

**Keputusan**: D-01 s.d. D-08 pada `docs/decision_log.md`.

**Hambatan**: tidak ada.

**Berikutnya**: langkah Setup 2–5.

## Sesi 2 — 2026-10-23

**Dikerjakan**
- Struktur folder sesuai spec §5.4 dibuat: package `src/pekael/` (config, core, models, loaders, splitters, vectorstores, services, evaluation), `scripts/`, `data/{source,processed,index,evaluation}`, `tests/{unit,integration,fixtures}`.
- `pyproject.toml` dibuat: package `pekael` (src layout, Python `>=3.11,<3.12`), konfigurasi pytest dengan marker `live` untuk test API sungguhan yang secara default dilewati. README awal ditambahkan.
- Virtual environment `.venv` dibuat dengan Python 3.11.9, pip ditingkatkan ke 26.2.2.
- Dependency runtime dan dev dipasang, lalu dipin (D-11, D-12):

  | Paket | Versi |
  |---|---|
  | langchain-core | 1.7.0 |
  | langchain-community | 0.4.2 |
  | langchain-text-splitters | 1.1.3 |
  | langchain-google-genai | 4.4.2 |
  | faiss-cpu | 1.15.1 (wheel pip Windows tersedia, Conda tidak diperlukan) |
  | numpy | 2.4.6 |
  | pymupdf | 2.0 |
  | pytesseract | 0.3.13 |
  | pillow | 13.0.0 |
  | streamlit | 1.66.1 |
  | pydantic | 2.14.1 |
  | python-dotenv | 1.2.4 |
  | pytest | 9.1.1 |

  Lock lengkap (96 paket): `requirements-lock.txt`.

**Hasil test**
- Perintah: `.venv\Scripts\python.exe -m pytest -v` → **5 lulus, 0 gagal**, 1 warning.
  - `test_core_imports`: semua paket inti dapat diimpor.
  - `test_runtime_does_not_import_evaluator_packages`: `pekael` tidak mengimpor `ragas` atau `langchain_openai` (FR-11).
  - `test_faiss_flat_l2_save_and_load`: LangChain FAISS membuat `IndexFlatL2` 768 dimensi, menyimpan dan memuat ulang, lalu menemukan dokumen yang benar dengan jarak ≈ 0.
  - `test_pymupdf_extracts_text_and_renders_page`: ekstraksi teks dan render halaman berfungsi.
  - `test_tesseract_ocr_indonesian`: bahasa `ind` tersedia, OCR membaca "PRAKTIK KERJA LAPANGAN" dari halaman yang dirender.
- Warning: `DeprecationWarning` bahwa `langchain-community` sedang di-sunset (lihat Hambatan).
- `pip check` → "No broken requirements found".

**File dibuat/diubah**
- `pyproject.toml`, `README.md`, `requirements.txt`, `requirements-dev.txt`, `requirements-lock.txt`
- `src/pekael/__init__.py` dan `__init__.py` di tiap subpackage
- `tests/unit/test_environment.py`, `.gitkeep` di `data/*` dan `tests/fixtures/`

**Keputusan**: D-11, D-12, Open Decision baru OD-15.

**Hambatan**
- Repo `langchain-community` diarsipkan upstream (issue langchain-ai/langchain-community#674, 2026). Wrapper FAISS LangChain berada di paket ini. Paket `langchain-faiss` di PyPI diperiksa: rilis 2024 oleh perorangan, ~1 kB, tanpa repo/provenance, dan bukan dari langchain-ai, sehingga **tidak dipakai**. Untuk saat ini `langchain-community==0.4.2` dipin karena terbukti berfungsi (OD-15).
- PyMuPDF 2.0 mewajibkan `pymupdf4llm`, `pymupdf-layout`, dan `onnxruntime`, sehingga instalasi lebih besar. Fungsi tetap berjalan, dicatat untuk pertimbangan hosting (OD-07).

**Berikutnya**: langkah Setup 6–9 (`.env.example`, konfigurasi + logging, kontrak inti dan factory, unit test dasar).

## Sesi 3 — 2026-10-23

**Dikerjakan**
- `.env.example` dibuat sesuai spec §8 dengan penyesuaian `FAISS_INDEX_PATH=data/index` (D-04) dan variabel baru `QUESTION_MAX_CHARS=500` (D-13).
- **Konfigurasi** (`config/settings.py`): `AppConfig` (Pydantic, immutable) memvalidasi tipe dan rentang nilai, termasuk `CHUNK_OVERLAP < CHUNK_SIZE` dan `LOG_LEVEL` yang valid. Nilai kosong atau placeholder `replace_with_...` dianggap belum diisi. Secret bertipe `SecretStr` sehingga tidak tampil di `repr`/log. `missing_runtime_settings()` menyediakan daftar variabel wajib yang belum diisi (bahan status FR-08).
- **`AppConfigurator.read_config()`**: membaca `.env` bila ada, environment variable sungguhan (secrets hosting) diprioritaskan. `create_manager_from_config()` masih kerangka (Sprint 3).
- **Logging** (`config/logging_config.py`): formatter yang menyamarkan nilai secret pada pesan dan traceback.
- **Kontrak inti dan Abstract Factory** sesuai class diagram:
  - ABC `BaseLoader`, `BaseSplitter`, `BaseVectorStore`,
  - `DocumentLoaderFactory.get_loader()`, `DocumentSplitterFactory.get_splitter()`, `VectorStoreFactory.get_vector_store()` yang mengembalikan `PDFLoader`, `RecursiveCharacterSplitter`, `FaissVectorStore`,
  - kerangka `ChatbotManager`, `GeminiModel`, `OcrService` (method inti melempar `NotImplementedError` dengan keterangan sprint pengisiannya).
- **`Chain` diimplementasikan penuh**: `add()`, `clear()`, `build()` (menyusun langkah menjadi LangChain `RunnableSequence`), `invoke()`. Langkah yang mengisi `ChainState.response` (mis. relevancy gate) menghentikan langkah berikutnya, sehingga fallback tidak memanggil Gemini.
- **Schemas** (`core/schemas.py`): `SourceReference`, `RetrievedDocument`, `ChatbotResponse`, `ResponseStatus`, `IndexingReport`, `IngestionReport`, `ChainState`.
- **`AdminAuthenticator`** diimplementasikan: satu akun, perbandingan constant-time (`hmac.compare_digest`), login nonaktif bila kredensial belum dikonfigurasi (FR-06).

**Hasil test**
- Perintah: `.venv\Scripts\python.exe -m pytest` → **50 lulus, 0 gagal**, 1 warning (sunset `langchain-community`, sama dengan sesi 2).

  | File test | Jumlah | Cakupan |
  |---|---|---|
  | `test_admin_auth.py` | 10 | kredensial benar/salah, case-sensitive, karakter non-ASCII, login nonaktif |
  | `test_chain.py` | 7 | urutan langkah, Runnable LangChain, short-circuit, chain kosong, clear, rebuild |
  | `test_config.py` | 11 | default spec, parsing, nilai kosong/placeholder, error yang menyebut nama variabel, secret tidak tampil, prioritas env vs `.env` |
  | `test_environment.py` | 5 | smoke test lingkungan (sesi 2) |
  | `test_factories.py` | 14 | ketiga factory, tipe tidak didukung, validasi parameter, ABC tidak dapat diinstansiasi |
  | `test_logging_config.py` | 3 | redaksi secret di pesan dan traceback |
- Import seluruh 26 modul `pekael` → berhasil (tidak ada circular import).

**File dibuat/diubah**
- `.env.example`
- `src/pekael/config/{settings,app_configurator,logging_config}.py`
- `src/pekael/core/{schemas,chain,chatbot_manager}.py`, `src/pekael/models/gemini_model.py`
- `src/pekael/loaders/{base,pdf_loader,factory}.py`, `src/pekael/splitters/{base,recursive_character_splitter,factory}.py`, `src/pekael/vectorstores/{base,faiss_vector_store,factory}.py`
- `src/pekael/services/{ocr_service,admin_auth}.py`
- `tests/unit/test_{config,logging_config,factories,chain,admin_auth}.py`

**Keputusan**: D-13, D-14.

**Hambatan**: tidak ada.

**Berikutnya**: langkah Setup 10–12 (README instalasi, kerangka `scripts/smoke_test_models.py`, audit secret).

## Sesi 4 — 2026-10-23

**Insiden secret (ditangani sebelum publikasi)**
- Commit lokal `726a6d7` memuat API key Gemini, API key OpenAI, dan password admin asli di `.env.example`. Commit berikutnya (`fix`) mengembalikan placeholder, tetapi nilai asli masih ada di riwayat commit.
- Push ditolak oleh GitHub Push Protection. Riwayat di `origin/main` diperiksa: **0 kemunculan** secret.
- Penanganan oleh pemilik: dua commit lokal digabung dengan `git reset --soft 8aa8a74` menjadi `4d0d78a` yang bersih, lalu di-push. Nilai asli dipindahkan ke `.env` (di-ignore).
- Sesuai NFR-01, kedua API key dan password admin dianjurkan untuk di-rotate karena nilainya sempat tersimpan di commit lokal dan terbaca saat pemeriksaan.
- Pencegahan: hook pre-commit pemindai secret (lihat di bawah).

**Dikerjakan**
- Parameter `langchain-google-genai` 4.4.2 diverifikasi dari source terpasang: `embed_documents` default `RETRIEVAL_DOCUMENT`, `embed_query` default `RETRIEVAL_QUERY` (sesuai spec §4.1 langkah 9 dan §4.3 langkah 3), dimensi diatur lewat `output_dimensionality`, nama model diterima tanpa awalan `models/`.
- `scripts/smoke_test_models.py`: tiga panggilan API kecil tanpa retry (chat, embedding dokumen, embedding query), memeriksa dimensi = `EMBEDDING_OUTPUT_DIMENSION` dan melaporkan norma L2 vektor (bahan OD-12), pesan error disamarkan dari secret.
- `scripts/check_secrets.py` + `.githooks/pre-commit`: memblokir commit file `.env` dan baris berisi pola key OpenAI/Google atau nilai `GEMINI_API_KEY`/`OPENAI_API_KEY`/`ADMIN_PASSWORD` non-placeholder. Mode `--all` memindai semua file yang dilacak git.
- README berisi prasyarat Windows, instalasi, konfigurasi, perlindungan secret, pengujian, dan struktur.
- Pemeriksaan `.env` (tanpa menampilkan nilai): `GEMINI_API_KEY` terisi, admin aktif, `OPENAI_API_KEY` terisi, `TESSERACT_CMD` kosong (Tesseract tidak ada di PATH, perlu diisi sebelum Sprint 1).

**Hasil test**
- `pytest` → **64 lulus, 0 gagal**, 1 warning (sunset `langchain-community`). Tambahan 14 test di `test_check_secrets.py` (deteksi key, placeholder diabaikan, file `.env` dilarang, `.env.example` di repo bersih).
- `check_secrets.py --all` → bersih.
- Uji hook pada repo git sementara: perubahan normal → exit 0, file `.env` dan key palsu → exit 1 dengan tiga temuan.
- `py_compile` kedua skrip → berhasil.

**File dibuat/diubah**
- `scripts/smoke_test_models.py`, `scripts/check_secrets.py`, `.githooks/pre-commit`, `tests/unit/test_check_secrets.py`, `README.md`

**Keputusan**: D-15.

**Hambatan**: insiden secret di atas (selesai ditangani).

**Berikutnya**
- Pemilik mengaktifkan hook: `git config core.hooksPath .githooks`.
- Pemilik mengisi `TESSERACT_CMD` di `.env`.
- Menjalankan `smoke_test_models.py` (OD-01, OD-02) setelah disetujui.
- Memasang dan mempin Ragas + smoke test tiga metrik (spec §10.4, OD-05, OD-06).

## Sesi 5 — 2026-10-23

**Dikerjakan**
- Smoke test Gemini live dijalankan (`scripts/smoke_test_models.py`). Hasil lengkap: [`smoke_tests.md`](smoke_tests.md).
- Dependency evaluasi dipasang dan dipin di `requirements-eval.txt`: `ragas==0.4.3`, `langchain-openai==1.7.2`, `openai==3.3.0`, `google-genai==2.33.0`. Dry-run sebelum instalasi memastikan tidak ada versi runtime yang berubah.
- **Inkompatibilitas ditemukan:** `ragas` 0.3.9–0.4.3 semuanya mengimpor `langchain_community.chat_models.vertexai` di `ragas/llms/base.py` baris 12. Modul itu tidak ada lagi di `langchain-community` 0.4.2, tetapi masih ada di 0.4.1, 0.4, dan 0.3.31 (diperiksa dari isi wheel tanpa instalasi). `langchain-community` 0.4.1 mensyaratkan `langchain-core>=1.0.1,<2.0.0`, sehingga cocok dengan `langchain-core==1.7.0`. → Pin diturunkan ke **`langchain-community==0.4.1`** (D-16). Efek samping: `DeprecationWarning` sunset tidak lagi muncul.
- API Ragas 0.4.3 yang dipakai (diverifikasi dari signature terpasang):

  | Metrik penelitian | Kelas Ragas 0.4.3 | Input `ascore()` |
  |---|---|---|
  | Faithfulness | `ragas.metrics.collections.Faithfulness(llm)` | `user_input`, `response`, `retrieved_contexts` |
  | Answer Relevance | `ragas.metrics.collections.AnswerRelevancy(llm, embeddings, strictness=3)` | `user_input`, `response` |
  | Context Recall | `ragas.metrics.collections.ContextRecall(llm)` | `user_input`, `retrieved_contexts`, `reference` |

  LLM evaluator: `ragas.llms.llm_factory(model, client=AsyncOpenAI(...))`. Embedding: `ragas.embeddings.GoogleEmbeddings(client=genai.Client(...), model="gemini-embedding-001")`.
- `scripts/smoke_test_ragas.py` dibuat: satu sampel fiktif, tiga metrik, `max_retries=0`.
- Test `test_evaluation_packages_import_when_installed` ditambahkan untuk menjaga pin `langchain-community` (dilewati otomatis bila paket evaluasi tidak terpasang).
- `requirements-lock.txt` diperbarui: 133 paket (lingkungan dev + eval).

**Hasil test**
- `pytest` → **65 lulus, 0 gagal**, tanpa warning.
- `check_secrets.py --all` → bersih.
- Smoke test Gemini → 3/3 lulus (percobaan ke-2, percobaan ke-1 chat gagal 503).
- Smoke test Ragas → 0/3, semua gagal `429 insufficient_quota / credit_balance_exhausted` dari OpenAI. Komponen embedding Gemini milik Ragas diuji terpisah → berhasil.

**File dibuat/diubah**
- `requirements.txt` (pin `langchain-community`), `requirements-eval.txt`, `requirements-lock.txt`
- `scripts/smoke_test_ragas.py`, `tests/unit/test_environment.py`
- `docs/technical/setup_log.md`, `docs/technical/smoke_tests.md`, `docs/scrum/setup_phase.md` (ditulis ulang dengan bahasa sederhana)

**Keputusan**: D-16, D-17, OD-01, OD-02 (sebagian), OD-05 diselesaikan.

**Hambatan**: saldo API OpenAI kosong, sehingga verifikasi evaluator LLM (OD-06) tertunda.
