# Log Teknis Sprint 3

> Ringkasan berbahasa sederhana: [`docs/scrum/sprint-03/`](../scrum/sprint-03/sprint_backlog.md)

## Sesi 1 — 6 November 2026

**FAISS vector store (S3-T03)** — `src/pekael/vectorstores/faiss_vector_store.py`
- Pembungkus LangChain `FAISS` (`langchain-community==0.4.1`, `DistanceStrategy.EUCLIDEAN_DISTANCE` → `IndexFlatL2`). OD-15 diputuskan: tetap memakai wrapper LangChain terpin (D-28).
- Tata letak (D-04): `<FAISS_INDEX_PATH>/ACTIVE`, `versions/<build_id>/{index.faiss, index.pkl, manifest.json}`. `build_id = <UTC %Y%m%dT%H%M%S%f>-<source_hash[:8]>`.
- `ingest_document(chunks)`: embed → tulis ke `versions/.building-<id>` → `manifest.json` → muat ulang dari folder sementara dan cek `ntotal == len(chunks)` → `os.replace` ke folder final → tulis `ACTIVE.tmp` lalu `os.replace` ke `ACTIVE` → muat → hapus versi lama di luar `keep_versions` (default 2, versi aktif tidak pernah dihapus). Kegagalan di langkah mana pun menghapus folder sementara dan melempar `VectorStoreError`, `ACTIVE` tidak berubah.
- `manifest.json`: `build_id`, `created_at`, `pekael_version`, `index_type`, `distance="squared_l2"`, `embedding_model`, `dimension`, `normalized`, `chunk_count`, `pages`, `sources` (file + hash), ditambah `build_info` (misalnya parameter chunk).
- `load()`: `IndexNotReadyError` bila `ACTIVE` belum ada, folder/manifest hilang, model embedding di manifest berbeda dengan pengaturan, atau file gagal dimuat. `load_local(..., allow_dangerous_deserialization=True)` hanya untuk folder buatan aplikasi sendiri.
- `get_relevant_document(query, k)`: memuat otomatis bila belum, mengembalikan `RetrievedDocument(document, distance)`.
- Exception baru di `vectorstores/base.py`: `VectorStoreError`, `IndexNotReadyError`.

**Satuan jarak (D-29)**: `IndexFlatL2.search` mengembalikan **kuadrat** jarak L2. Untuk vektor ternormalisasi, nilainya `2 − 2·cos`, rentang 0–4 secara teori, dan sekitar 0,3–0,8 pada data Pekael. EXP-002 memakai `faiss.IndexFlatL2` langsung sehingga nilainya sama satuannya. `RETRIEVAL_MAX_L2_DISTANCE` dikalibrasi dalam satuan ini.

**Test**: `pytest` → **156 lulus, 0 gagal** (baru: `test_faiss_vector_store.py` 13 test, embedding tiruan `DeterministicFakeEmbedding`).

## Sesi 2 — 7 November 2026

**OCR halaman tambahan (S3-T01)**: gambar 110 dpi vs `page_NNN.txt`. Koreksi ditulis ke `data/corrections/565a9929ea00/page_{022,023,024,025,027,028}.txt`. Rincian: [`scrum/sprint-03/pemeriksaan_ocr.md`](../scrum/sprint-03/pemeriksaan_ocr.md). `inspect_pdf.py` (29 halaman) → kolom koreksi "ya" untuk 15 halaman.

**Halaman final (S3-T02)**: `.env` `KNOWLEDGE_BASE_PAGES=4-16,22-25,27-28` (diubah dengan skrip yang hanya mengganti baris tersebut). `inspect_chunks.py --configs 1000:150` → 19 halaman, 33 potongan, min 36, rata-rata 687, maks 995 karakter, 0 tanpa bagian, 0 duplikat.

**Splitter (D-31)**: `section` direset bila nomor halaman tidak berurutan (halaman dilewati). Pola judul baru `^LAMPIRAN [A-Z][A-Z /&,()-]{3,80}$`. Sebelum perbaikan `p022-c01` berlabel "B. Nilai Akhir / C. SISTEMATIKA LAPORAN PKL" (terbawa dari hal. 16) dan `p027`/`p028` berlabel "C. SISTEMATIKA LAPORAN PKL". Sesudah: `p022-c01` "C. SISTEMATIKA LAPORAN PKL", `p027`/`p028` "LAMPIRAN INSTRUMEN PENILAIAN PKL".

**GeminiModel (S3-T04)** — `src/pekael/models/gemini_model.py`
- `generate_response(prompt, system_prompt=None) -> str`: `[SystemMessage, HumanMessage]` ke `ChatGoogleGenerativeAI(temperature=0, timeout=30, max_retries=0, reasoning_effort=...)`.
- `LLMError(kind)`: `quota` (429/RESOURCE_EXHAUSTED), `auth` (401/403/API_KEY_INVALID/PERMISSION_DENIED), `unavailable` (503/500/DEADLINE_EXCEEDED/timeout), `empty`, `other`. Hanya `unavailable` dicoba ulang (1 kali, jeda 2 s). Pesan galat tidak menyertakan teks penyedia.
- Konfigurasi baru `GEMINI_REASONING_EFFORT` (kosong = bawaan model).

**Prompt policy (S3-T05, D-30)** — `src/pekael/core/prompts.py`: `SYSTEM_PROMPT` (aturan spec §4.4), `FALLBACK_MESSAGE` (teks spec), `format_context` (`[n] (halaman PDF p, section)`), `build_user_prompt`, `parse_answer` (penanda `TIDAK_DITEMUKAN`, baris `SUMBER: n, m` → nomor konteks valid saja, `None` bila tidak ada).

**Uji langsung prompt** (konteks dari `chunks_1000_150.jsonl`, 4 potongan per pertanyaan, tanpa FAISS):

| Pertanyaan | Hasil | Rujukan | Waktu |
|---|---|---|---|
| Berapa SKS minimal untuk bisa ikut PKL? | "Mahasiswa dapat menjadi peserta PKL jika telah memenuhi minimal 100 SKS." | hal. 10 | 3,80 s |
| Kapan batas akhir pendaftaran PKL semester ini? | `TIDAK_DITEMUKAN` | — | 9,75 s |
| Kalau nilai saya 74, apakah saya lulus PKL? | 74 = B (bobot 3,0), di bawah syarat minimal B+ | hal. 16, 11 | 9,61 s |

**EXP-003**: `thinking_budget=0` → `400 INVALID_ARGUMENT` pada `gemini-3.5-flash-lite`. `reasoning_effort` `minimal`/`low` diuji pada 3 pertanyaan yang sama, hasil di `docs/experiment_log.md`.

**Test**: `pytest` → **185 lulus, 0 gagal** (baru: `test_gemini_model.py` 14, `test_prompts.py` 12, 2 test splitter, 1 test config). Peringatan `LangChainDeprecationWarning` (`.text()` dipanggil sebagai method) diperbaiki dengan membaca `.text` sebagai property.

## Sesi 3 — 8 November 2026

**Alur tanya-jawab (S3-T06)** — `src/pekael/core/rag_steps.py`
- `RagSteps(vector_store, llm, system_prompt, retrieval_k, max_distance, question_max_chars).build_chain()` menambahkan enam langkah ke `Chain`: `validate_input` (strip, kosong, > `QUESTION_MAX_CHARS`) → `retrieve` (`get_relevant_document(q, k)`, simpan `state.distances`) → `relevancy_gate` (buang potongan dengan jarak > `RETRIEVAL_MAX_L2_DISTANCE`, tolak bila tidak ada yang tersisa, nonaktif bila kosong) → `build_prompt` (`format_context`, `build_user_prompt`) → `generate` (`GeminiModel.generate_response`) → `validate_citations` (`parse_answer`, `SourceReference` dari metadata potongan yang disebut di baris `SUMBER:`, cuplikan ≤ 200 karakter).
- Pemetaan galat: `IndexNotReadyError` → `unavailable` + `INDEX_NOT_READY`. `EmbeddingError`/`LLMError` digolongkan dengan `classify_error` (termasuk `__cause__`): `quota`, `unavailable`, `auth` → `unavailable` dengan pesan masing-masing. `empty`/`other`/`VectorStoreError` → `error`. Pesan di `src/pekael/core/messages.py`.
- `ChatbotResponse` dan `ChainState` mendapat kolom `distances` (jarak semua potongan terambil sebelum ambang) untuk log dan kalibrasi.

**Perakitan (S3-T07)**
- `ChatbotManager.__init__` menerima `retrieval_k`, `max_distance`, `question_max_chars` dan membangun rantai bawaan bila `chain` kosong. `initialize_knowledge_base` = `loader.load` → `splitter.split` → `vector_store.ingest_document`, `IngestionReport` dengan peringatan halaman OCR tanpa file koreksi. `generate_response` membungkus galat tak terduga menjadi `error` + `UNEXPECTED_ERROR` (`logger.exception`), mencatat status, jumlah rujukan, jarak terdekat, dan waktu, tanpa teks pertanyaan.
- `AppConfigurator.create_manager_from_config` merakit lewat ketiga factory, menolak (`ConfigError`) bila `GEMINI_API_KEY` kosong.
- Skrip baru: `scripts/build_knowledge_base.py` dan `scripts/ask.py`.

**Knowledge base pertama**: `build_knowledge_base.py` → build `20261102T180419398924-565a9929` (timestamp UTC asli), 19 halaman OCR, 33 potongan, 10,4 s. Peringatan halaman 7, 9, 12, 15 tanpa file koreksi: halaman tersebut sudah diverifikasi benar pada Sprint 1 sehingga tidak memerlukan koreksi.

**Uji langsung dan kondisi gagal**: [`smoke_tests.md` §6](smoke_tests.md). Peringatan `UserWarning: Model 'gemini-3.5-flash-lite' uses fixed sampling defaults, the sampling parameter(s) temperature will be ignored` (D-36). Gemini membuka jawaban dengan salam pada 2 dari 6 pertanyaan, aturan prompt no. 1 ditambah (D-35), uji ulang 3 pertanyaan tanpa salam.

**Kalibrasi ambang (S3-T08, EXP-004)**: `scripts/run_threshold_experiment.py --generate` (jeda 4 s antarpanggilan) → ambang 0,64. `.env` `RETRIEVAL_MAX_L2_DISTANCE=0.64` (hanya baris tersebut diubah dengan skrip). Hasil di `experiment_log.md`. Lembar pemeriksaan PO dibuat dari `exp004.json`: [`scrum/sprint-03/pemeriksaan_jawaban.md`](../scrum/sprint-03/pemeriksaan_jawaban.md). `export_docs.py` mendapat judul untuk `pemeriksaan_jawaban`, dan baris tabel yang memuat NIM/NIP diberi `<w:cantSplit/>` agar blok tanda tangan tidak terpotong antarhalaman.

**Panggilan API sesi ini**: 1 panggilan embedding batch (build), sekitar 60 embedding kueri, dan sekitar 50 panggilan Gemini (uji langsung + EXP-004). Tidak ada penolakan 429.

**Test**: `pytest` → **224 lulus, 0 gagal** (baru: `tests/unit/test_rag_steps.py` 26, `tests/unit/test_chatbot_manager.py` 9, `tests/integration/test_rag_pipeline.py` 2, `test_export_docs.py` 2). Run pertama: 2 gagal (`test_index_not_ready_returns_status_without_calling_llm`, `test_question_before_build_reports_missing_knowledge_base`) karena cabang `IndexNotReadyError` tidak berhenti sehingga pesan tertimpa fallback. Diperbaiki dengan `return state`.

