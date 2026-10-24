# Fase Setup — Catatan Pengerjaan

> Fase Setup (spec §17 Phase 2) menyiapkan lingkungan dan kerangka kode sebelum Sprint 1. Fase ini bukan sprint, tetapi dicatat agar seluruh proses dapat ditelusuri.
> Rujukan langkah: `implementation_plan.md` §5.

## Checklist Setup

| # | Langkah | Status | Bukti |
|---|---|---|---|
| 0 | `.gitignore` dan `implementation_plan.md` | Selesai | Ditinjau pemilik 2026-10-25 |
| 1 | Prasyarat OS: Python 3.11, Tesseract + bahasa `ind` | Selesai | Lihat log 2026-10-25 |
| 2 | Struktur folder dan package | Selesai | `src/pekael/*`, `scripts/`, `data/*`, `tests/*` |
| 3 | `pyproject.toml` | Selesai | Install editable `pekael 0.1.0` berhasil |
| 4 | `.venv` + dependency + pin versi | Selesai | `requirements.txt`, `requirements-dev.txt`, `requirements-lock.txt`; `pip check` bersih |
| 5 | Smoke test tanpa API (FAISS, PyMuPDF, Tesseract) | Selesai | `pytest`: 5 lulus, 0 gagal |
| 6 | `.env.example` | Selesai | Placeholder saja, tanpa secret |
| 7 | `AppConfig`, configurator, logging | Selesai | `test_config.py`, `test_logging_config.py` |
| 8 | Kontrak inti dan factory minimal | Selesai | 26 modul `pekael` dapat diimpor |
| 9 | Unit test dasar | Selesai | `pytest`: 50 lulus, 0 gagal |
| 10 | README instalasi | Belum | |
| 11 | Kerangka `scripts/smoke_test_models.py` | Belum | |
| 12 | Audit secret | Belum | |

## Log Pengerjaan

### 2026-10-25

**Dikerjakan**
- Spec dibaca dan dianalisis; `implementation_plan.md` disusun dan dinyatakan lengkap oleh pemilik proyek.
- `.gitignore` diisi: secret, data penelitian, PDF, dan file bantu Claude Code dikecualikan karena repo bersifat public.
- Python **3.11.9** dipasang via `winget` (scope user) di `C:\Users\dwiki\AppData\Local\Programs\Python\Python311\python.exe`. Python 3.13 tetap ada tetapi tidak dipakai untuk proyek ini.
- Tesseract OCR **5.4.0.20240606** (build UB Mannheim) dipasang via `winget` di `C:\Program Files\Tesseract-OCR\`.
- Data bahasa `ind.traineddata` (8.279.230 byte) diunduh dari `github.com/tesseract-ocr/tessdata` (branch `main`) dan disalin ke folder `tessdata`. Hasil `tesseract --list-langs`: `eng`, `ind`, `osd`.
- Struktur dokumentasi Scrum dibuat di `docs/scrum/`.

**Keputusan**: D-01 s.d. D-08 pada `docs/decision_log.md`.

**Hambatan**: tidak ada.

**Berikutnya**: langkah Setup 2–5.

### 2026-10-25 (sesi 2)

**Dikerjakan**
- Struktur folder sesuai spec §5.4 dibuat: package `src/pekael/` (config, core, models, loaders, splitters, vectorstores, services, evaluation), `scripts/`, `data/{source,processed,index,evaluation}`, `tests/{unit,integration,fixtures}`.
- `pyproject.toml` dibuat: package `pekael` (src layout, Python `>=3.11,<3.12`), konfigurasi pytest dengan marker `live` untuk test API sungguhan yang secara default dilewati. README awal ditambahkan.
- Virtual environment `.venv` dibuat dengan Python 3.11.9; pip ditingkatkan ke 26.2.2.
- Dependency runtime dan dev dipasang, lalu dipin (D-11, D-12):

  | Paket | Versi |
  |---|---|
  | langchain-core | 1.7.0 |
  | langchain-community | 0.4.2 |
  | langchain-text-splitters | 1.1.3 |
  | langchain-google-genai | 4.4.2 |
  | faiss-cpu | 1.15.1 (wheel pip Windows tersedia; Conda tidak diperlukan) |
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
  - `test_tesseract_ocr_indonesian`: bahasa `ind` tersedia; OCR membaca "PRAKTIK KERJA LAPANGAN" dari halaman yang dirender.
- Warning: `DeprecationWarning` bahwa `langchain-community` sedang di-sunset (lihat Hambatan).
- `pip check` → "No broken requirements found".

**File dibuat/diubah**
- `pyproject.toml`, `README.md`, `requirements.txt`, `requirements-dev.txt`, `requirements-lock.txt`
- `src/pekael/__init__.py` dan `__init__.py` di tiap subpackage
- `tests/unit/test_environment.py`, `.gitkeep` di `data/*` dan `tests/fixtures/`

**Keputusan**: D-11, D-12; Open Decision baru OD-15.

**Hambatan**
- Repo `langchain-community` diarsipkan upstream (issue langchain-ai/langchain-community#674, 2026). Wrapper FAISS LangChain berada di paket ini. Paket `langchain-faiss` di PyPI diperiksa: rilis 2024 oleh perorangan, ~1 kB, tanpa repo/provenance, dan bukan dari langchain-ai, sehingga **tidak dipakai**. Untuk saat ini `langchain-community==0.4.2` dipin karena terbukti berfungsi (OD-15).
- PyMuPDF 2.0 mewajibkan `pymupdf4llm`, `pymupdf-layout`, dan `onnxruntime`, sehingga instalasi lebih besar. Fungsi tetap berjalan; dicatat untuk pertimbangan hosting (OD-07).

**Berikutnya**: langkah Setup 6–9 (`.env.example`, konfigurasi + logging, kontrak inti dan factory, unit test dasar).

### 2026-10-25 (sesi 3)

**Dikerjakan**
- `.env.example` dibuat sesuai spec §8 dengan penyesuaian `FAISS_INDEX_PATH=data/index` (D-04) dan variabel baru `QUESTION_MAX_CHARS=500` (D-13).
- **Konfigurasi** (`config/settings.py`): `AppConfig` (Pydantic, immutable) memvalidasi tipe dan rentang nilai, termasuk `CHUNK_OVERLAP < CHUNK_SIZE` dan `LOG_LEVEL` yang valid. Nilai kosong atau placeholder `replace_with_...` dianggap belum diisi. Secret bertipe `SecretStr` sehingga tidak tampil di `repr`/log. `missing_runtime_settings()` menyediakan daftar variabel wajib yang belum diisi (bahan status FR-08).
- **`AppConfigurator.read_config()`**: membaca `.env` bila ada; environment variable sungguhan (secrets hosting) diprioritaskan. `create_manager_from_config()` masih kerangka (Sprint 3).
- **Logging** (`config/logging_config.py`): formatter yang menyamarkan nilai secret pada pesan dan traceback.
- **Kontrak inti dan Abstract Factory** sesuai class diagram:
  - ABC `BaseLoader`, `BaseSplitter`, `BaseVectorStore`;
  - `DocumentLoaderFactory.get_loader()`, `DocumentSplitterFactory.get_splitter()`, `VectorStoreFactory.get_vector_store()` yang mengembalikan `PDFLoader`, `RecursiveCharacterSplitter`, `FaissVectorStore`;
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
