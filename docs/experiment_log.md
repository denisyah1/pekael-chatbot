# Experiment Log — Pekael

Catatan eksperimen yang memengaruhi hasil Ragas/UAT (NFR-06): chunking, dimensi embedding, normalisasi, `k`, threshold, prompt, dan model. Hasil yang sudah dicatat tidak diubah, eksperimen ulang memakai ID baru.

## Format Entri

### EXP-NNN — _[judul singkat]_

| | |
|---|---|
| Tanggal | |
| Sprint | |
| Tujuan | |
| Konfigurasi | `CHUNK_SIZE=…`, `CHUNK_OVERLAP=…`, `RETRIEVAL_K=…`, model, dimensi, normalisasi, build_id indeks |
| Data uji | _[set pertanyaan + versinya]_ |
| Prosedur | |
| Hasil | _[angka/tabel aktual]_ |
| Kesimpulan | |
| Keputusan terkait | D-xx / OD-xx |

## Entri

### EXP-001 — Resolusi render untuk OCR (200 vs 300 dpi)

| | |
|---|---|
| Tanggal | 2026-10-26 |
| Sprint | 1 |
| Tujuan | Menentukan `OCR_RENDER_DPI` untuk Buku Pedoman PKL 2025 (hasil scan JPEG ≈ 200 dpi) |
| Konfigurasi | Tesseract 5.4.0, `ind+eng`, render grayscale PyMuPDF, `OCR_MIN_TEXT_CHARS_PER_PAGE=40` |
| Data uji | `Pedoman-PKL-2025.pdf` (SHA-256 `565a9929…8a39`), halaman 4–6 |
| Prosedur | `inspect_pdf.py --pages 4-6 --dpi 200` dan `--dpi 300`, bandingkan keyakinan, waktu, dan selisih kata terhadap gambar asli |
| Hasil | Keyakinan rata-rata 200 dpi: 91,8 / 91,6 / 91,6, 300 dpi: 91,9 / 90,3 / 91,0. Waktu 200 dpi: 6,3 / 5,7 / 4,1 s, 300 dpi: 7,3 / 7,3 / 5,2 s. Selisih kata: 200 dpi salah pada "BAB I" (`BABI`) dan judul "C." (`Cc.`), 300 dpi salah pada "PKL/PKL." (`PKL/PEL,`), "lembaga;" (`lembaga,`), dan judul "C." (`.`). Keduanya salah membaca kata miring "hard-skill" (`/ard-skill`). |
| Kesimpulan | 200 dpi (sama dengan resolusi scan, tanpa pembesaran gambar) sedikit lebih akurat pada tanda baca dan ±20% lebih cepat. Kesalahan yang tersisa ditangani lewat pemeriksaan manual. |
| Keputusan terkait | D-20 (`OCR_RENDER_DPI=200`) |
