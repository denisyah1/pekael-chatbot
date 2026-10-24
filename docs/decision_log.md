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

## Penyelesaian Open Decision

| OD | Tanggal | Hasil | Bukti | Rujukan |
|---|---|---|---|---|
| — | | | | |
