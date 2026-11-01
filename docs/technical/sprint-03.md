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
