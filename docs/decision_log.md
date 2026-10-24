# Decision Log — Pekael

Catatan keputusan teknis yang tidak tertulis di `project_spec.md` atau yang menyelesaikan Open Decision. Entri tidak dihapus; keputusan yang berubah ditandai *Digantikan oleh D-xx*.

## Keputusan

| ID | Tanggal | Keputusan | Status | Alasan | Sprint/fase |
|---|---|---|---|---|---|
| D-01 | 2026-10-25 | Python 3.11 64-bit (terpasang 3.11.9) dalam `.venv` | Disetujui pemilik | Stabilitas FAISS/Ragas/LangChain; spec §3.1 | Plan |
| D-02 | 2026-10-25 | PyMuPDF untuk ekstraksi teks native dan render halaman untuk OCR | Disetujui pemilik | Satu library, tanpa Poppler; lisensi AGPL → OD-11 | Plan |
| D-03 | 2026-10-25 | Repo GitHub public; file bantu Claude Code tidak di-push | Disetujui pemilik | Diterapkan di `.gitignore` | Plan |
| D-04 | 2026-10-25 | Indeks FAISS berversi + penunjuk `ACTIVE`; `FAISS_INDEX_PATH=data/index` | Disetujui pemilik | Swap atomik di Windows; rollback mudah | Plan |
| D-05 | 2026-10-25 | Normalisasi L2 embedding sebelum `IndexFlatL2` | Disetujui sebagai rencana; diuji di Sprint 2 (OD-12) | Threshold jarak lebih stabil | Plan |
| D-06 | 2026-10-25 | Dependency dipecah: runtime / dev / eval | Disetujui pemilik | FR-11, NFR-03 | Plan |
| D-07 | 2026-10-25 | `pyproject.toml` untuk package `src/pekael` | Disetujui pemilik | Import konsisten untuk app, script, dan test | Plan |
| D-08 | 2026-10-25 | Dokumentasi Scrum di `docs/scrum/`, keputusan di `docs/decision_log.md`, eksperimen di `docs/experiment_log.md` | Disetujui pemilik | Spec §16; kebutuhan laporan dan validasi per sprint | Plan |
| D-09 | 2026-10-25 | Tesseract 5.4.0.20240606 (UB Mannheim) + `ind.traineddata` dari repo `tesseract-ocr/tessdata` | Terpasang | Model standar, sama dengan yang dibundel installer | Setup |
| D-10 | 2026-10-25 | Claude Code tidak melakukan `git commit`/`push`; hanya memberi arahan, dan pemilik yang menjalankan | Disetujui pemilik | Kendali penuh pemilik atas riwayat repo | Setup |
| D-11 | 2026-10-25 | Dependency langsung dipin `==` di `requirements.txt` / `requirements-dev.txt`; seluruh dependency transitif dikunci di `requirements-lock.txt`. `faiss-cpu` dipasang via pip (tanpa Conda) | Diterapkan | Spec §3.1; smoke test lulus pada Python 3.11.9 / Windows 11 | Setup |
| D-12 | 2026-10-25 | Tetap memakai `langchain-community==0.4.2` untuk wrapper FAISS; **tidak** memakai paket PyPI `langchain-faiss` | Diterapkan, menunggu OD-15 | Upstream diarsipkan, tetapi versi terpin berfungsi. `langchain-faiss` tidak resmi dan tanpa provenance (risiko supply chain) | Setup |
| D-13 | 2026-10-25 | Variabel baru `QUESTION_MAX_CHARS` (default 500). Nilai env kosong atau berawalan `replace_with_` dianggap belum diisi | Diterapkan | FR-01 mewajibkan batas panjang input lewat konfigurasi, tetapi variabelnya belum ada di spec §8. Placeholder dicegah terbaca sebagai key asli | Setup |
| D-14 | 2026-10-25 | `Chain` menyusun langkah menjadi LangChain `RunnableSequence`; langkah yang mengisi `ChainState.response` menghentikan langkah sisanya. Schema memakai dataclass; `AppConfig` memakai Pydantic | Diterapkan | Workflow deterministik sesuai class diagram; fallback tanpa memanggil Gemini (spec §4.3 langkah 6) | Setup |
| D-15 | 2026-10-25 | Hook pre-commit `.githooks/pre-commit` → `scripts/check_secrets.py` (stdlib saja); diaktifkan per clone dengan `git config core.hooksPath .githooks` | Diterapkan, menunggu aktivasi pemilik | Mencegah terulangnya secret ter-commit (insiden sesi 4); NFR-01 | Setup |

## Penyelesaian Open Decision

| OD | Tanggal | Hasil | Bukti | Rujukan |
|---|---|---|---|---|
| — | | | | |
