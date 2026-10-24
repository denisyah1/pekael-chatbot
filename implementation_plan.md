# Implementation Plan — Pekael

> **Turunan dari:** `project_spec.md` (sumber acuan utama; bila bertentangan, spec yang berlaku)
> **Fase:** Output Phase 1 — PLAN (spec §17), menjadi pegangan Phase 2 — SETUP dan Phase 3 — BUILD
> **Tanggal dibuat:** 2026-10-25
> **Status:** Ditinjau dan dinyatakan lengkap oleh pemilik proyek (2026-10-25). Usulan D-04 s.d. D-08 dianggap disetujui; rincian di `docs/decision_log.md`.

---

## 1. Keputusan yang Sudah Diambil pada Fase Plan

Keputusan berikut tidak ada di spec atau melengkapinya. Masing-masing dicatat agar dapat ditelusuri (NFR-06).

| ID | Keputusan | Status | Alasan |
|---|---|---|---|
| D-01 | Python **3.11 64-bit** dalam virtual environment `.venv` | Disetujui pemilik | Sesuai rekomendasi spec §3.1; ekosistem FAISS/Ragas/LangChain paling stabil di 3.11. Python 3.13 yang terpasang di laptop tidak dipakai untuk proyek ini. |
| D-02 | **PyMuPDF** (`pymupdf`) untuk ekstraksi teks native per halaman dan render halaman ke gambar untuk OCR | Disetujui pemilik | Satu library untuk dua kebutuhan, kualitas ekstraksi baik, tidak butuh Poppler di Windows. Catatan lisensi: AGPL-3.0, lihat OD-11. |
| D-03 | Repository GitHub **public**; file bantu Claude Code (`CLAUDE.md`, `.claude/`, `MEMORY.md`) tidak di-push | Disetujui pemilik | Sudah diterapkan di `.gitignore`. |
| D-04 | Indeks FAISS disimpan **berversi** + file penunjuk `ACTIVE` | Usulan | Rename folder yang tujuannya sudah ada gagal di Windows. Menulis file penunjuk lalu `os.replace` bersifat atomik di Windows dan Linux, dan rollback cukup dengan mengganti isi penunjuk. |
| D-05 | Vektor embedding **dinormalisasi L2** sebelum masuk `IndexFlatL2` | Usulan (OD-12) | `gemini-embedding-001` pada dimensi < 3072 tidak dinormalisasi otomatis. Setelah normalisasi, jarak L2 setara monoton dengan cosine similarity sehingga threshold lebih stabil. Indeks tetap `IndexFlatL2` sesuai spec. |
| D-06 | Dependency dipecah: `requirements.txt` (runtime), `requirements-dev.txt` (test), `requirements-eval.txt` (Ragas/OpenAI) | Usulan | FR-11 & NFR-03: chatbot dan deployment tidak perlu paket/kunci evaluator. |
| D-07 | `pyproject.toml` untuk package `src/pekael` (install editable) dan konfigurasi pytest | Usulan | Layout `src/` pada spec §5.4 membutuhkan package yang terpasang agar import konsisten di app, script, dan test. |
| D-08 | Folder `docs/`: dokumentasi Scrum di `docs/scrum/` (planning, backlog, review, retrospective, lembar validasi per sprint), `docs/decision_log.md`, dan `docs/experiment_log.md` | Disetujui pemilik | Spec §16 mewajibkan logbook sprint dan catatan keputusan; dibutuhkan untuk laporan dan validasi per sprint. |

---

## 2. Arsitektur

### 2.1 Pemetaan class diagram → modul

| Kelas diagram | Modul | Catatan implementasi |
|---|---|---|
| `Client` | `app.py` | Streamlit; `st.session_state` hanya untuk tampilan riwayat sesi (FR-10), tidak pernah dikirim ke prompt. `ChatbotManager` di-cache dengan `st.cache_resource`. |
| `AppConfigurator` | `config/app_configurator.py` | `read_config()` membaca `.env`/environment/`st.secrets` → `AppConfig`; `create_manager_from_config()` merakit seluruh komponen melalui factory. |
| `AppConfig` | `config/settings.py` | Pydantic model; validasi tipe dan nilai saat startup. Secret bertipe `SecretStr` agar tidak tercetak di log/repr. |
| `ChatbotManager` | `core/chatbot_manager.py` | Memiliki `system_prompt`, `loader`, `splitter`, `vector_store`, `llm`, dan `chain`. Tanpa memory. |
| `Chain` | `core/chain.py` | Daftar langkah eksplisit; `build()` menyusunnya menjadi LCEL `RunnableSequence` (dari `RunnableLambda`). Relevancy gate menandai state `fallback` dan langkah berikutnya dilewati, sehingga Gemini tidak dipanggil. |
| Prompt policy | `core/prompts.py` | System prompt (§4.4) dan template konteks. Teks fallback dibaca dari konfigurasi. |
| Schemas | `core/schemas.py` | `ChatbotResponse`, `SourceReference`, `RetrievedDocument`, `IngestionReport`, `IndexingReport`, `ChainState`. |
| `GeminiModel` (`LLM`) | `models/gemini_model.py` | Membungkus `ChatGoogleGenerativeAI`; memetakan error (429, auth, timeout) ke exception domain. |
| Embeddings (pendukung) | `models/embeddings.py` | Membungkus `GoogleGenerativeAIEmbeddings` (task type dokumen/query, `output_dimensionality`) dan normalisasi L2 (D-05). Tambahan kecil di luar diagram, diperlukan oleh `FaissVectorStore`. |
| `BaseLoader` / `PDFLoader` / `DocumentLoaderFactory` | `loaders/` | `PDFLoader` memakai PyMuPDF per halaman; halaman dengan teks < `OCR_MIN_TEXT_CHARS_PER_PAGE` dikirim ke `OcrService`. |
| `OcrService` (pendukung) | `services/ocr_service.py` | `pytesseract` + path `TESSERACT_CMD`; hanya dipanggil saat ingestion. |
| `BaseSplitter` / `RecursiveCharacterSplitter` / `DocumentSplitterFactory` | `splitters/` | Membungkus `RecursiveCharacterTextSplitter`; memberi `chunk_id` stabil (`<source_hash[:8]>-p<page>-c<n>`). |
| `BaseVectorStore` / `FaissVectorStore` / `VectorStoreFactory` | `vectorstores/` | LangChain `FAISS` (default `IndexFlatL2`); `similarity_search_with_score` mengembalikan jarak L2. Manifest disimpan di samping indeks. |
| Admin | `services/admin_auth.py` | Satu akun; `hmac.compare_digest`; login nonaktif bila kredensial belum dikonfigurasi (FR-06). |
| Pengelolaan sumber | `services/source_manager.py` | Validasi upload, build ke folder versi baru, verifikasi muat-ulang, pindahkan penunjuk `ACTIVE` (FR-07). |
| Evaluasi | `evaluation/dataset.py`, `evaluation/ragas_evaluator.py` | Hanya diimpor oleh `scripts/run_ragas_evaluation.py`. Import Ragas/OpenAI bersifat lazy agar runtime tidak membutuhkannya. |

### 2.2 Urutan `Chain` runtime

```text
validate_input → retrieve(k) → relevancy_gate(max_l2) ─┬─ lolos → format_context → build_prompt → generate → validate_citations → ChatbotResponse
                                                        └─ gagal → fallback ChatbotResponse (tanpa panggilan Gemini)
```

`validate_citations` membuang rujukan yang tidak berasal dari chunk hasil retrieval (FR-05, NFR-02). Rujukan dibentuk dari metadata, bukan dari teks LLM.

### 2.3 Tata letak indeks (D-04)

```text
data/index/
├── ACTIVE                         # berisi satu baris: build_id aktif
└── versions/
    └── 20261025T101500-ab12cd34/  # <timestamp>-<source_hash[:8]>
        ├── index.faiss
        ├── index.pkl              # docstore LangChain (pickle; hanya file buatan sendiri)
        └── manifest.json          # model embedding, dimensi, normalisasi, chunk params, source file + hash, waktu build, versi app
```

`FAISS_INDEX_PATH` pada spec §8 bernilai `data/index/current`; diusulkan menjadi `data/index` (root), dan versi aktif dibaca dari `ACTIVE`. Dua versi terakhir dipertahankan untuk rollback.

---

## 3. Dependency

Versi **belum dipin** pada dokumen ini. Paket dipasang di Python 3.11, smoke test dijalankan, lalu versi yang lulus dipin dengan `==` (spec §3.1). Hasil pin dicatat di `docs/decisions.md`.

| File | Paket |
|---|---|
| `requirements.txt` | `langchain-core`, `langchain-community`, `langchain-text-splitters`, `langchain-google-genai`, `faiss-cpu`, `numpy`, `pymupdf`, `pytesseract`, `pillow`, `streamlit`, `pydantic`, `python-dotenv` |
| `requirements-dev.txt` | `-r requirements.txt`, `pytest` |
| `requirements-eval.txt` | `-r requirements.txt`, `ragas`, `langchain-openai`, `datasets` (jika diminta versi Ragas) |
| `environment.yml` | **Hanya dibuat jika** `pip install faiss-cpu` gagal di Windows (spec §3.1) |

Executable OS (bukan paket pip): **Python 3.11** dan **Tesseract OCR** (installer UB Mannheim, dengan data bahasa `ind` dan `eng`).

---

## 4. Traceability: Kebutuhan → Modul → Test

| Kebutuhan | Modul utama | Test |
|---|---|---|
| FR-01 Input | `core/chain.py` (`validate_input`), `app.py` | `unit/test_chain.py` |
| FR-02 Retrieval | `vectorstores/faiss_vector_store.py` | `unit/test_faiss_vector_store.py`, `integration/test_pipeline.py` |
| FR-03 Generasi grounded | `core/prompts.py`, `models/gemini_model.py` | `unit/test_prompts.py`, `unit/test_chatbot_manager.py` (LLM mock) |
| FR-04 Fallback | `core/chain.py` (`relevancy_gate`) | `unit/test_chain.py` (threshold diterima/ditolak) |
| FR-05 Rujukan | `core/chain.py` (`validate_citations`), `core/schemas.py` | `unit/test_citations.py` |
| FR-06 Admin | `services/admin_auth.py` | `unit/test_admin_auth.py` |
| FR-07 Update dokumen | `services/source_manager.py` | `unit/test_source_manager.py`, `integration/test_index_swap.py` |
| FR-08 Status sistem | `core/chatbot_manager.py` (`health()`), `app.py` | `unit/test_chatbot_manager.py` |
| FR-09 OCR bersyarat | `loaders/pdf_loader.py`, `services/ocr_service.py` | `unit/test_pdf_loader.py` (fixture PDF + OCR mock) |
| FR-10 Tanpa memory | `core/chatbot_manager.py`, `app.py` | `unit/test_chatbot_manager.py` (prompt tidak memuat pesan sebelumnya) |
| FR-11 Ragas terpisah | `evaluation/`, `scripts/run_ragas_evaluation.py` | `unit/test_dataset.py`; import test bahwa `pekael` tidak mengimpor `ragas` |
| PBI-01 OCR | `loaders/`, `services/ocr_service.py`, `scripts/inspect_pdf.py` | Laporan ekstraksi Sprint 1 |
| PBI-02 Penyaringan konten | Proses manual + validasi PO | Bukti validasi di logbook |
| PBI-03 Split & embedding | `splitters/`, `models/embeddings.py` | `unit/test_splitter.py`, `unit/test_embeddings.py` |
| PBI-04 FAISS | `vectorstores/` | `unit/test_faiss_vector_store.py` |
| PBI-05 Retrieval chain | `core/` | `integration/test_pipeline.py` |
| PBI-06 UI | `app.py` | Functional test manual (spec §15.3) |
| PBI-07 Rujukan di UI | `app.py`, `core/schemas.py` | Functional test manual |
| PBI-08 Admin update | `app.py`, `services/` | Functional test manual + unit test |

Unit dan integration test **tidak memanggil API sungguhan**: embedding memakai `DeterministicFakeEmbedding` dari `langchain_core`, LLM memakai fake/mock. Test API sungguhan hanya ada di `scripts/smoke_test_models.py` dan dijalankan manual.

---

## 5. Rencana Phase 2 — SETUP

Urutan kerja (spec §17 Phase 2). Setiap langkah dilaporkan sebelum lanjut.

1. **Prasyarat OS** (dipasang oleh pemilik atau dengan persetujuan): Python 3.11 (`winget install Python.Python.3.11`), Tesseract UB Mannheim + data `ind`.
2. **Struktur folder** sesuai spec §5.4 + `docs/`, `.gitkeep` pada `data/*`, `tests/{unit,integration,fixtures}`.
3. **`pyproject.toml`** (metadata package, src layout, konfigurasi pytest).
4. **Dependency**: buat `.venv` dengan Python 3.11 → pasang `requirements-dev.txt` → smoke test → pin versi.
5. **Smoke test tanpa API**: import semua paket; FAISS `IndexFlatL2` add/search/save/load dengan fake embedding; PyMuPDF membuka fixture PDF; `pytesseract.get_tesseract_version()`.
6. **`.env.example`** sesuai spec §8 (placeholder saja) dengan penyesuaian `FAISS_INDEX_PATH=data/index`.
7. **Konfigurasi & logging**: `AppConfig`, `AppConfigurator.read_config()`, logger dengan filter yang menyamarkan nilai secret.
8. **Kontrak inti & factory minimal**: semua ABC (`BaseLoader`, `BaseSplitter`, `BaseVectorStore`), tiga factory, `schemas.py`, kerangka `Chain`, `ChatbotManager`, `GeminiModel`. Method yang baru diisi di Sprint selanjutnya melempar `NotImplementedError` dengan pesan jelas.
9. **Unit test dasar**: konfigurasi, factory mengembalikan tipe yang benar, schema, admin auth, `Chain.add/clear/build/invoke` dengan langkah dummy.
10. **README**: instalasi Python 3.11, venv, Tesseract (path Windows), FAISS, `.env`, cara menjalankan test.
11. **`scripts/smoke_test_models.py`** (kerangka): verifikasi model Gemini dan OpenAI; **dijalankan oleh pemilik** setelah `.env` berisi key baru (OD-01, OD-05, OD-06).
12. **Audit secret**: `git status` dan pencarian pola key sebelum commit.

**Kriteria selesai Setup:** environment terpasang ulang dari file dependency, `pytest` lulus, tidak ada secret di repo, tidak ada deployment.

---

## 6. Rencana Phase 3 — BUILD (ringkas per sprint)

| Sprint | File yang diisi | Hasil yang dapat diperiksa |
|---|---|---|
| 1 | `loaders/pdf_loader.py`, `services/ocr_service.py`, `scripts/inspect_pdf.py`, `docs/logbook.md` | Laporan per halaman (native/OCR, jumlah karakter), teks hasil di `data/processed/`, catatan verifikasi angka/tanggal/tabel, validasi PO |
| 2 | `splitters/*`, `models/embeddings.py` | Statistik chunk, uji dimensi, penanganan 429, eksperimen chunk_size/overlap di logbook (OD-02, OD-03) |
| 3 | `vectorstores/*`, `models/gemini_model.py`, `core/chain.py`, `core/prompts.py`, `core/chatbot_manager.py`, `config/app_configurator.py`, `scripts/build_knowledge_base.py` | Pipeline CLI berjalan end-to-end, distribusi jarak in-scope vs out-of-scope, threshold awal (OD-04) |
| 4 | `app.py`, `services/admin_auth.py`, `services/source_manager.py`, test unit/integration | UI lokal untuk mahasiswa + admin, swap indeks atomik, laporan test |
| 5 | `evaluation/*`, `scripts/run_ragas_evaluation.py` (dry-run), `data/evaluation/README.md` | Dataset tervalidasi, threshold/parameter dibekukan, dry-run Ragas, perbandingan hosting (OD-07, OD-10) |
| 6 | Konfigurasi deployment + dokumentasi akhir | Deploy, hasil Ragas per baris + rerata, suite out-of-scope terpisah, rekap UAT |

---

## 7. Risiko Kompatibilitas

| Area | Risiko | Mitigasi |
|---|---|---|
| FAISS di Windows | Wheel pip tidak tersedia untuk kombinasi Python/OS | Python 3.11 (D-01); fallback ke Miniforge + `environment.yml` |
| Tesseract | Executable tidak ada di PATH; data `ind` belum terpasang | `TESSERACT_CMD` di konfigurasi; cek `get_languages()` di smoke test |
| `langchain-google-genai` | Parameter `task_type`/`output_dimensionality` berubah antarversi | Verifikasi pada versi terpin; test dimensi vektor |
| LangChain FAISS | `load_local` mensyaratkan `allow_dangerous_deserialization=True` | Hanya memuat indeks dari folder versi buatan sendiri; dicatat di `decisions.md` |
| Ragas | Nama metric/field dataset berubah antarversi | Pin versi; fungsi mapping eksplisit; dry-run Sprint 5 |
| Model Gemini | `gemini-3.5-flash-lite` belum terverifikasi tersedia/gratis | Smoke test Setup; tidak ada auto-switch ke model berbayar |
| Streamlit + rebuild indeks | Manager ter-cache masih memegang indeks lama setelah swap | Muat ulang manager setelah swap berhasil (Sprint 4) |

---

## 8. Open Decisions

OD-01 s.d. OD-10 tetap seperti spec §18. Tambahan dari fase Plan:

| ID | Keputusan | Paling lambat | Catatan |
|---|---|---|---|
| OD-11 | Lisensi repository | Sebelum deployment publik (Sprint 6) | PyMuPDF berlisensi AGPL-3.0; repo public memudahkan kepatuhan. Pilih lisensi yang kompatibel (mis. AGPL-3.0) atau ganti ke `pypdfium2` (permisif) dengan persetujuan. |
| OD-12 | Normalisasi L2 embedding (D-05) | Sprint 2 | Diuji bersama OD-02; disimpan di manifest indeks. |
| OD-13 | Apakah dataset ground truth dan buku panduan boleh dipublikasikan di repo public | Sprint 5 | Default: tidak di-commit (sudah di `.gitignore`). Hanya `ground_truth.example.jsonl` yang public. |
| OD-14 | Butir UAT no. 3 ("rujukan pada *setiap* jawaban") vs jawaban fallback tanpa rujukan | Sebelum distribusi UAT | Dibahas bersama OD-08 dengan pembimbing. |

---

## 9. Hal yang Tidak Dikerjakan Tanpa Persetujuan

Mengikuti spec §18: tidak mengganti teknologi FIXED, tidak menambah database/agent/memory/login mahasiswa, tidak mengubah metrik Ragas atau UAT, tidak melakukan upgrade berbayar, tidak melakukan deployment, dan tidak menulis credential ke file mana pun selain `.env` lokal milik pemilik.
