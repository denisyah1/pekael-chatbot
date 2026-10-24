# Fase Setup — Catatan Pengerjaan

> Fase Setup (spec §17 Phase 2) menyiapkan lingkungan dan kerangka kode sebelum Sprint 1. Fase ini bukan sprint, tetapi dicatat agar seluruh proses dapat ditelusuri.
> Rujukan langkah: `implementation_plan.md` §5.

## Checklist Setup

| # | Langkah | Status | Bukti |
|---|---|---|---|
| 0 | `.gitignore` dan `implementation_plan.md` | Selesai | Ditinjau pemilik 2026-10-25 |
| 1 | Prasyarat OS: Python 3.11, Tesseract + bahasa `ind` | Selesai | Lihat log 2026-10-25 |
| 2 | Struktur folder dan package | Belum | |
| 3 | `pyproject.toml` | Belum | |
| 4 | `.venv` + dependency + pin versi | Belum | |
| 5 | Smoke test tanpa API (FAISS, PyMuPDF, Tesseract) | Belum | |
| 6 | `.env.example` | Belum | |
| 7 | `AppConfig`, configurator, logging | Belum | |
| 8 | Kontrak inti dan factory minimal | Belum | |
| 9 | Unit test dasar | Belum | |
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
