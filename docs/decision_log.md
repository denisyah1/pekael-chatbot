# Decision Log — Pekael

Catatan keputusan teknis yang tidak tertulis di `project_spec.md` atau yang menyelesaikan Open Decision. Entri tidak dihapus, keputusan yang berubah ditandai *Digantikan oleh D-xx*.

## Keputusan

| ID | Tanggal | Keputusan | Status | Alasan | Sprint/fase |
|---|---|---|---|---|---|
| D-01 | 2026-10-23 | Python 3.11 64-bit (terpasang 3.11.9) dalam `.venv` | Disetujui pemilik | Stabilitas FAISS/Ragas/LangChain, spec §3.1 | Plan |
| D-02 | 2026-10-23 | PyMuPDF untuk ekstraksi teks native dan render halaman untuk OCR | Disetujui pemilik | Satu library, tanpa Poppler, lisensi AGPL → OD-11 | Plan |
| D-03 | 2026-10-23 | Repo GitHub public, file bantu Claude Code tidak di-push | Disetujui pemilik | Diterapkan di `.gitignore` | Plan |
| D-04 | 2026-10-23 | Indeks FAISS berversi + penunjuk `ACTIVE`, `FAISS_INDEX_PATH=data/index` | Disetujui pemilik | Swap atomik di Windows, rollback mudah | Plan |
| D-05 | 2026-10-23 | Normalisasi L2 embedding sebelum `IndexFlatL2` | Disetujui sebagai rencana, diuji di Sprint 2 (OD-12) | Threshold jarak lebih stabil | Plan |
| D-06 | 2026-10-23 | Dependency dipecah: runtime / dev / eval | Disetujui pemilik | FR-11, NFR-03 | Plan |
| D-07 | 2026-10-23 | `pyproject.toml` untuk package `src/pekael` | Disetujui pemilik | Import konsisten untuk app, script, dan test | Plan |
| D-08 | 2026-10-23 | Dokumentasi Scrum di `docs/scrum/`, keputusan di `docs/decision_log.md`, eksperimen di `docs/experiment_log.md` | Disetujui pemilik | Spec §16, kebutuhan laporan dan validasi per sprint | Plan |
| D-09 | 2026-10-23 | Tesseract 5.4.0.20240606 (UB Mannheim) + `ind.traineddata` dari repo `tesseract-ocr/tessdata` | Terpasang | Model standar, sama dengan yang dibundel installer | Setup |
| D-10 | 2026-10-23 | Claude Code tidak melakukan `git commit`/`push`, hanya memberi arahan, dan pemilik yang menjalankan | Disetujui pemilik | Kendali penuh pemilik atas riwayat repo | Setup |
| D-11 | 2026-10-23 | Dependency langsung dipin `==` di `requirements.txt` / `requirements-dev.txt`, seluruh dependency transitif dikunci di `requirements-lock.txt`. `faiss-cpu` dipasang via pip (tanpa Conda) | Diterapkan | Spec §3.1, smoke test lulus pada Python 3.11.9 / Windows 11 | Setup |
| D-12 | 2026-10-23 | Tetap memakai `langchain-community==0.4.2` untuk wrapper FAISS, **tidak** memakai paket PyPI `langchain-faiss` | Diterapkan, menunggu OD-15 | Upstream diarsipkan, tetapi versi terpin berfungsi. `langchain-faiss` tidak resmi dan tanpa provenance (risiko supply chain) | Setup |
| D-13 | 2026-10-23 | Variabel baru `QUESTION_MAX_CHARS` (default 500). Nilai env kosong atau berawalan `replace_with_` dianggap belum diisi | Diterapkan | FR-01 mewajibkan batas panjang input lewat konfigurasi, tetapi variabelnya belum ada di spec §8. Placeholder dicegah terbaca sebagai key asli | Setup |
| D-14 | 2026-10-23 | `Chain` menyusun langkah menjadi LangChain `RunnableSequence`, langkah yang mengisi `ChainState.response` menghentikan langkah sisanya. Schema memakai dataclass, `AppConfig` memakai Pydantic | Diterapkan | Workflow deterministik sesuai class diagram, fallback tanpa memanggil Gemini (spec §4.3 langkah 6) | Setup |
| D-15 | 2026-10-23 | Hook pre-commit `.githooks/pre-commit` → `scripts/check_secrets.py` (stdlib saja), diaktifkan per clone dengan `git config core.hooksPath .githooks` | Diterapkan, menunggu aktivasi pemilik | Mencegah terulangnya secret ter-commit (insiden sesi 4), NFR-01 | Setup |
| D-16 | 2026-10-23 | `langchain-community` diturunkan dari 0.4.2 ke **0.4.1**. Paket evaluasi dipin: `ragas==0.4.3`, `langchain-openai==1.7.2`, `openai==3.3.0`, `google-genai==2.33.0` | Diterapkan | Ragas 0.3.9–0.4.3 mengimpor `langchain_community.chat_models.vertexai`, yang dihapus di 0.4.2. Versi 0.4.1 cocok dengan `langchain-core==1.7.0`, 65 test lulus | Setup |
| D-17 | 2026-10-23 | Evaluasi Ragas memakai API `ragas.metrics.collections` (Faithfulness, AnswerRelevancy, ContextRecall) dengan `llm_factory` + `AsyncOpenAI` dan embedding `GoogleEmbeddings` (Gemini) | Diterapkan, evaluator OpenAI belum terverifikasi | API yang direkomendasikan di Ragas 0.4.3 (spec §10.4), embedding Gemini menghindari biaya OpenAI tambahan | Setup |
| D-18 | 2026-10-23 | Dokumentasi dua lapis: `docs/scrum/` berbahasa sederhana untuk laporan, rincian teknis di `docs/technical/` | Disetujui pemilik | Permintaan pemilik agar dokumen laporan mudah dipahami | Setup |
| D-19 | 2026-10-23 | Sprint 1–3 masing-masing 1 minggu (Sprint 1: 23–29 Okt, Sprint 2: 30 Okt–5 Nov, Sprint 3: 6–12 Nov 2026), Sprint 4–6 tetap 2 minggu sesuai spec §12. Fase Setup dan Sprint Planning 1 berada dalam periode Sprint 1. Pekerjaan Sprint 1 yang sudah tuntas di fase Setup (repo, struktur, smoke test FAISS) dicatat Done dengan rujukan ke fase Setup | Ditetapkan pemilik | Pengembangan dimulai lebih lambat dari rencana awal (awal Oktober), sehingga tiga sprint pertama dipadatkan | Sprint 1 |
| D-20 | 2026-10-26 | OCR: render grayscale `OCR_RENDER_DPI=200`, keyakinan per halaman dari Tesseract (`image_to_data`) dipakai untuk mengurutkan prioritas pemeriksaan manual (< 85). Perapian teks konservatif: tanda hubung tidak diubah, baris daftar dan judul pendek (≤ 60 karakter) tetap terpisah | Diterapkan | EXP-001, hasil ekstraksi halaman 5 dan 19 | Sprint 1 |
| D-21 | 2026-10-26 | Ekspor dokumen Scrum ke Word/PDF dengan pandoc 3.12.1 (`scripts/export_docs.py`). Template bersih `docs/templates/reference.docx` dibangun dari template Lembar Validasi milik pemilik (hanya gaya, header, logo, dan pengaturan halaman). Judul header/footer ditentukan per jenis dokumen. NIM/NIP diisi dari `.env` saat ekspor. Template asli di root dan folder `docs/export/` di-ignore git | Disetujui pemilik | Laporan dan lembar validasi per sprint perlu format Word/PDF yang seragam. Repo public, sehingga data pribadi tidak boleh ikut | Sprint 1 |

## Penyelesaian Open Decision

| OD | Tanggal | Hasil | Bukti | Rujukan |
|---|---|---|---|---|
| OD-01 | 2026-10-23 | **Sebagian.** `gemini-3.5-flash-lite` tersedia dan menjawab dalam Bahasa Indonesia. Belum final: status free tier/kuota perlu dicek pemilik di dashboard Google AI Studio, lalu disetujui | Smoke test Gemini percobaan 2 | `technical/smoke_tests.md` §2 |
| OD-02 | 2026-10-23 | **Sebagian.** Dimensi 768 didukung (`output_dimensionality`). Pilihan final tetap di Sprint 2 | Smoke test Gemini | `technical/smoke_tests.md` §2 |
| OD-05 | 2026-10-23 | **Selesai.** Answer Relevancy memakai embedding Gemini lewat `ragas.embeddings.GoogleEmbeddings`, `text-embedding-3-small` tidak dipakai | Uji komponen embedding Ragas | `technical/smoke_tests.md` §3 |
| OD-06 | — | **Tertunda.** Saldo OpenAI kosong (429 `insufficient_quota`) | Smoke test Ragas | `technical/smoke_tests.md` §3 |
