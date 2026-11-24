# Log Teknis Sprint 5

> Ringkasan berbahasa sederhana: [`docs/scrum/sprint-05/`](../scrum/sprint-05/sprint_backlog.md)

## Sesi 1 — 20 November 2026

**Dokumen knowledge base tambahan (S5-T02, D-53)**
- Sumber: `data/source/Knowledge_Base_PKL_PTIK_UNJ-2.pdf` (8 halaman, 188 KB, semua halaman teks digital, tidak ada gambar). Di-ignore Git (`data/source/*`, `*.pdf`) karena memuat nomor kontak Admin Prodi dan Kaprodi.
- `.env`: `KNOWLEDGE_BASE_EXTRA_PATHS=data/source/Knowledge_Base_PKL_PTIK_UNJ-2.pdf` (daftar dipisah koma). `.env.example` diberi baris kosong yang sama.
- `config/settings.py`: field `knowledge_base_extra_paths`, properti `extra_knowledge_paths -> list[Path]`.
- `loaders/base.py`, `loaders/pdf_loader.py`: argumen `all_pages=True` mengabaikan `KNOWLEDGE_BASE_PAGES` (milik Buku Pedoman).
- `core/chatbot_manager.py`: `initialize_knowledge_base(source_path, pages=None, on_progress=None, extra_paths=())`. Setiap dokumen dimuat lalu dipotong sendiri, `build_info["extra_paths"]` dicatat di manifest. `IngestionReport.extra_sources` berisi nama file dokumen tambahan.
- `vectorstores/faiss_vector_store.py`: manifest punya `documents` (per dokumen: `source_file`, `source_hash`, `pages`, `chunks_per_page`, `total_pages`, `chunk_count`) dengan urutan pemuatan, Buku Pedoman pertama. Field lama `pages`, `chunks_per_page`, `total_pages` tetap menggambarkan Buku Pedoman agar build lama dan peta halaman tetap terbaca. Metode baru `documents()`.
- `core/schemas.py`: `document_name()` dipindah dari UI ke inti. `core/prompts.py`: label konteks menjadi `[n] (Pedoman PKL 2025, halaman PDF 10, <bagian>)`, aturan 8 menyebut "buku pedoman dan knowledge base PKL Prodi".
- `ui/student_page.py`: `manifest_documents()`, `source_groups()`, `render_source_tabs()`, `top_pill()`. Sidebar menampilkan setiap dokumen. Label "Dari panduan PKL", expander "Lihat kutipan sumbernya", kutipan menyebut nama dokumen bila rujukan berasal dari lebih dari satu dokumen. `ui/theme.py`: `quote(..., document=None)`.
- `ui/admin_page.py`: `extra_paths()` (dari manifest aktif, cadangan dari `.env`), `run_build(..., extras)`, catatan dokumen tambahan pada tab "Ganti buku pedoman", peta halaman per dokumen, riwayat versi menyebut semua dokumen, uji pertanyaan menampilkan halaman per dokumen.
- `scripts/build_knowledge_base.py`: memakai `extra_knowledge_paths`.
- `scripts/run_threshold_experiment.py`: halaman dokumen tambahan ditulis `KB<n>`, peringkat hanya dihitung untuk halaman Buku Pedoman, opsi `--threshold` untuk menjawab dengan ambang tetap (sebelumnya selalu titik tengah), hasil mencatat `documents` dan `answer_threshold`.

**Pembangunan knowledge base**
- `python scripts/build_knowledge_base.py` → 13,2 s, 27 halaman (teks digital 8, OCR 19), 61 potongan (Buku Pedoman 33, dokumen tambahan 28), build `20261124T053813125686-565a9929`. Peringatan halaman OCR tanpa file koreksi `[7, 9, 12, 15]` sama seperti build sebelumnya, tidak berkaitan dengan dokumen tambahan.
- `created_at` manifest diubah ke `2026-11-20T05:38:17+00:00` mengikuti linimasa sprint, nilai asli disimpan di `created_at_original`.
- Versi `20261104T043244948591-565a9929` (hanya Buku Pedoman) tetap tersimpan untuk rollback.

**EXP-010**
- `python scripts/run_threshold_experiment.py --generate --pause 4 --threshold 0.64 --output data/processed/Pedoman-PKL-2025/exp010.json`
- Hit@4 halaman Buku Pedoman 34/36 (no. 22 dan 24 diambil dari dokumen tambahan). Jarak terbesar dalam cakupan 0,557, terkecil non-PKL 0,663, titik tengah 0,61.
- Dengan ambang 0,64: dalam cakupan 36/36 `answered`, L2 dan L5 `answered` (dokumen tambahan hlm. 3 dan 6), L1, L3, L4 `out_of_scope`, N1–N3 ditolak ambang. Waktu median 1,68 s, maks 2,35 s.

**Perbaikan pembersih sapaan (D-54)**
- Uji langsung "Siapa koordinator PKL Prodi PTIK saat ini?": keluaran mentah Gemini "Hai, kalau kamu mau tahu ..., sekarang dijabat sama Bambang Satrio, S.Pd., M.Kom. Jadi, ..." tampil sebagai "Pd., M.Kom. Jadi, ...". Penyebab: `_LEADING_GREETING` menghapus dari "Hai" sampai tanda baca pertama.
- `core/prompts.py`: `_GREETING_QUESTION` (sapaan + pertanyaan basa-basi yang diakhiri "?", dihapus utuh) dan `_GREETING_WORD` (hanya kata sapaan, opsional "kak", "semua", lalu huruf pertama sisa kalimat dijadikan kapital).
- "Berapa nomor WhatsApp admin prodi PTIK?" → `answered` dengan nomor dari bagian F dokumen tambahan.

**Evaluator Ragas Groq (S5-T03, D-52)**
- Tidak ada paket baru: Groq menyediakan API yang kompatibel dengan OpenAI, sehingga `openai==3.3.0` (sudah ada di `requirements-eval.txt`) dipakai dengan `base_url=https://api.groq.com/openai/v1`.
- `config/settings.py`: `openai_api_key`, `openai_eval_model`, `openai_eval_embedding_model` diganti `groq_api_key` (secret), `groq_eval_model` (bawaan `openai/gpt-oss-120b`), `groq_base_url`. `secret_values()` memuat `groq_api_key`.
- `.env`: `GROQ_API_KEY=` (kosong, diisi pemilik) dan `GROQ_EVAL_MODEL=openai/gpt-oss-120b` ditambahkan. Baris `OPENAI_*` lama dibiarkan dan tidak lagi dibaca kode. `.env.example`: `OPENAI_*` diganti `GROQ_API_KEY=replace_with_your_groq_key`, `GROQ_EVAL_MODEL`.
- `scripts/check_secrets.py`: pola `gsk_[A-Za-z0-9]{20,}` dan `GROQ_API_KEY=` bernilai.
- `scripts/smoke_test_ragas.py`: `llm_factory(config.groq_eval_model, provider="openai", client=AsyncOpenAI(api_key=..., base_url=config.groq_base_url, max_retries=0))`. Embedding Answer Relevancy tetap `GoogleEmbeddings` (OD-05).
- `python scripts/smoke_test_ragas.py` → `Variabel berikut belum diisi di .env: GROQ_API_KEY`, exit 2.

**Uji**
- `pytest` → **340 lulus, 0 gagal** (327 sebelumnya). Test baru: dokumen tambahan dimuat penuh dan dipotong terpisah, build tanpa dokumen tambahan, `KNOWLEDGE_BASE_EXTRA_PATHS`, field Groq dan redaksinya, manifest per dokumen, build lama satu dokumen, `all_pages`, pengelompokan rujukan, `top_pill`, sapaan di depan isi, tiga pola secret Groq.

## Sesi 2 — 21 November 2026

**Ragas dengan Groq (S5-T03)**
- `python scripts/smoke_test_ragas.py` → `ragas 0.4.3 | evaluator LLM: openai/gpt-oss-120b (Groq) | embeddings: gemini-embedding-001 (Gemini)`. Faithfulness 1.000 (4,24 s), Answer Relevancy 0.992 (6,44 s), Context Recall 1.000 (1,96 s), `3/3 metrik berjalan`, exit 0. Mode instructor bawaan `llm_factory(provider="openai")` bekerja dengan endpoint Groq.

**Pertanyaan koordinator PKL berstatus `out_of_scope` (D-55)**
- Keluaran mentah (2 dari 4 percobaan): "...Koordinator PKL Prodi PTIK kita adalah Bambang Satrio, S.Pd., M.Kom. ... menghubungi beliau kalau ada pertanyaan seputar PKL yang jawabannya tidak ada di panduan ..." → log `Answer is a redirection without the marker, treated as one`.
- `core/prompts.py`: `_ADMITS_MISSING` diberi lookbehind `(?<!yang )(?<!jawabannya )(?<!jawaban )`. `_GREETING_WORD` menerima kata pendamping berulang `kak|kakak|kamu|juga|semua|semuanya|teman-teman` dengan batas kata (`Halo kamus` tidak terpotong).
- Uji langsung sesudah perbaikan: "siapa koordinator pkl", "Siapa koordinator PKL?", "siapa koordinator pkl ya kak" → `answered`. "Kapan batas akhir pendaftaran PKL semester ini?" → `out_of_scope`.

**EXP-011**
- `python scripts/run_threshold_experiment.py --generate --pause 4 --threshold 0.64 --output data/processed/Pedoman-PKL-2025/exp011.json` → dalam cakupan 36/36 `answered`, L4 dan L5 `answered`, L1–L3 `out_of_scope`, N1–N3 ditolak ambang, median 1,67 s, maks 9,28 s (no. 25).

**Uji**
- `pytest` → **342 lulus, 0 gagal** (test baru: kalimat yang menggambarkan pertanyaan lain bukan arahan, kata pendamping sapaan).

## Sesi 3 — 22 November 2026

**Dataset evaluasi v1 (S5-T04, D-56)**
- `scripts/build_ground_truth.py` (tanpa panggilan API) menyimpan 40 entri: `PKL` (id, topik, jenis, pertanyaan, jawaban acuan, sumber, catatan) dan `NON_PKL` (N1–N4). Keluaran:
  - `data/evaluation/ground_truth.jsonl` (di-ignore Git): `id`, `version`, `category` (`pkl`/`non_pkl`), `topic`, `question_type`, `user_input`, `reference`, `reference_contexts` (teks utuh halaman sumber: `data/processed/Pedoman-PKL-2025/page_NNN.txt` atau teks PyMuPDF dokumen tambahan), `reference_sources` (`source_file`, `page`), `note`. Total teks konteks rujukan 152.486 karakter.
  - `docs/scrum/sprint-05/dataset_ground_truth.md`: lembar validasi tanpa halaman sumber.
- Pertanyaan N1–N3 sama dengan EXP-004, N4 baru ("Laptop apa yang bagus untuk kuliah?").
- `scripts/export_docs.py`: pemetaan `dataset_ground_truth` → "Lampiran: Lembar Validasi Dataset Evaluasi". Ekspor `--sprint 5 --pdf` → 10 halaman, placeholder NIM/NIP terisi, salinan `dataset_ground_truth_5_DeniM.docx/.pdf`.
- `tests/unit/test_ground_truth.py`: 40 id unik, teks pertanyaan sama dengan `sprint-04/pertanyaan_uji.md`, setiap entri PKL punya sumber, lembar tanpa rujukan halaman dan tanpa titik koma.
- `pytest` → **344 lulus, 0 gagal**.

## Sesi 4 — 23 November 2026

- `docs/scrum/sprint-01/product_backlog_utama.md` (baru): PBI-01 sampai PBI-08 dari spec §13 dan tabel keterlacakan `implementation_plan.md` §4, Definition of Done dari spec §14. File Sprint 1 lain tidak diubah.
- `scripts/export_docs.py`: argumen `--only NAME` (hanya dokumen dengan nama file tersebut), pemetaan `product_backlog_utama` → "Lampiran: Product Backlog Utama".
- `export_docs.py --sprint 1 --only product_backlog_utama --pdf` → 3 halaman, placeholder terisi, salinan `product_backlog_utama_1_DeniM.docx/.pdf`. Waktu ubah file ekspor Sprint 1 lain tetap sama.
- `pytest` → **344 lulus, 0 gagal**.
