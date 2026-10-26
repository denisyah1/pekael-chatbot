# Log Teknis Sprint 1

> Ringkasan berbahasa sederhana: [`docs/scrum/sprint-01/`](../scrum/sprint-01/sprint_backlog.md)

## Identitas Dokumen Sumber

| | |
|---|---|
| File | `Pedoman-PKL-2025.pdf` (di-ignore git melalui pola `*.pdf`) |
| Ukuran | 7.282.498 byte |
| SHA-256 | `565a9929ea00a99971c4fc423b0de0cf7e5cbb652acf092bf4f56141a8cc8a39` |
| Metadata PDF | format PDF 1.4, creator `BIZHUB 363 BP-3 Lt.2`, producer `KONICA MINOLTA bizhub 363`, creationDate `2025-08-05T11:59:03Z` |
| Halaman | 29, ukuran 595 × 842 pt (A4), rotasi 0, tidak terenkripsi |
| Layer teks | 0 karakter di semua halaman, setiap halaman berisi tepat 1 gambar |
| Gambar per halaman | JPEG 1653 × 2338 px (≈ 200 dpi pada A4) |

## Sesi 1 — 23 Oktober 2026

**Pemeriksaan awal** (PyMuPDF 2.0, hanya membaca):
- `page.get_text()` → 0 karakter pada halaman 1–29, seluruhnya di bawah `OCR_MIN_TEXT_CHARS_PER_PAGE=40`, sehingga semua halaman akan melalui jalur OCR.
- Render 60 dpi halaman 1, 5, 15 untuk inspeksi visual: scan lurus, kontras baik, latar bersih. Halaman 1 adalah sampul (grafis + judul). Halaman 5 dan 15 berisi paragraf, subjudul berhuruf (B., C.), dan daftar bernomor/berhuruf. Tidak ada tabel pada halaman sampel.
- Resolusi ≈ 200 dpi berada di bawah anjuran umum Tesseract (≈ 300 dpi). Render ulang ke resolusi lebih tinggi saat OCR diuji pada S1-T05/S1-T09 (EXP berikutnya bila memengaruhi hasil).

**Catatan**
- File dipindahkan pemilik ke `data/source/Pedoman-PKL-2025.pdf`.
- Sprint 1–3 berdurasi 1 minggu (D-19).

## Sesi 2 — 26 Oktober 2026

**Implementasi**
- `services/ocr_service.py`: `OcrService.check_available()` (versi Tesseract + cek data bahasa), `image_to_text()` → `OcrResult` (teks dari `image_to_string`, keyakinan rata-rata dan jumlah kata dengan keyakinan < 60 dari `image_to_data`). Exception `OcrUnavailableError`.
- `loaders/pdf_loader.py`: `PDFLoader.open_pdf()` (validasi: file ada, PDF terbaca, tidak berpassword, ≥ 1 halaman → `DocumentLoadError`), `extract_page()` (teks native bila ≥ `min_text_chars`, selain itu render grayscale pada `ocr_dpi` lalu OCR), `to_document()`. Metadata per halaman: `source_file`, `source_hash` (SHA-256), `page` (1-based), `total_pages`, `extraction_method`, dan untuk OCR `ocr_mean_confidence`, `ocr_low_confidence_words`.
- `loaders/text_cleaning.py`: `clean_page_text()` — NFC, ligatur, karakter tak terlihat, spasi ganda, gabung baris terbungkus, baris daftar (`1.`, `a.`, `b)`, `IV.`, `-`) dan judul pendek (≤ 60 karakter tanpa tanda baca penutup, diikuti huruf kapital) tetap di baris sendiri, gabung paragraf yang terputus di tengah kalimat (paragraf sebelumnya tanpa `.:;?!)` dan paragraf berikutnya diawali huruf kecil). Tanda hubung tidak diubah.
- Konfigurasi baru `OCR_RENDER_DPI` (default 200, EXP-001).
- `scripts/inspect_pdf.py`: menulis `page_NNN.txt`, `page_NNN.raw.txt`, `report.json`, `report.md` ke `data/processed/<nama pdf>/` (di-ignore git). Opsi `--dpi`, `--pages`, `--out`.

**Test**
- `pytest` → **90 lulus, 0 gagal**. Baru: `test_text_cleaning.py` (10), `test_pdf_loader.py` (11, memakai PDF buatan + OCR palsu), `test_ocr_service.py` (4, dua di antaranya memakai Tesseract sungguhan).

**Ekstraksi penuh** — `inspect_pdf.py data\source\Pedoman-PKL-2025.pdf`
- Tesseract 5.4.0.20240606, `ind+eng`, 200 dpi, 29/29 halaman `tesseract_ocr`, total 111.1 s.
- Keyakinan OCR: min 76.0, maks 92.6, rata-rata 89.6.

| Hal. | Karakter | Keyakinan | Kata ragu | Detik |
|---|---|---|---|---|
| 1 | 119 | 76.0 | 3 | 2.24 |
| 2 | 693 | 89.5 | 2 | 3.51 |
| 3 | 977 | 92.6 | 0 | 3.19 |
| 4 | 2137 | 91.8 | 0 | 6.28 |
| 5 | 2103 | 91.6 | 5 | 5.44 |
| 6 | 1294 | 91.6 | 0 | 3.92 |
| 7 | 1148 | 91.6 | 0 | 3.78 |
| 8 | 1557 | 91.5 | 2 | 4.39 |
| 9 | 1397 | 90.9 | 0 | 4.89 |
| 10 | 1554 | 91.7 | 1 | 4.62 |
| 11 | 1535 | 91.8 | 1 | 4.32 |
| 12 | 369 | 92.5 | 0 | 1.77 |
| 13 | 1122 | 88.9 | 8 | 4.71 |
| 14 | 1051 | 88.0 | 10 | 4.11 |
| 15 | 509 | 91.1 | 0 | 2.46 |
| 16 | 714 | 90.6 | 1 | 3.27 |
| 17 | 1617 | 92.2 | 1 | 4.06 |
| 18 | 933 | 90.8 | 3 | 3.01 |
| 19 | 1498 | 82.8 | 20 | 5.09 |
| 20 | 1434 | 91.4 | 2 | 3.93 |
| 21 | 1746 | 90.4 | 11 | 4.67 |
| 22 | 971 | 89.9 | 2 | 3.61 |
| 23 | 1646 | 91.8 | 1 | 6.7 |
| 24 | 661 | 89.2 | 5 | 2.46 |
| 25 | 544 | 91.1 | 0 | 3.16 |
| 26 | 376 | 92.2 | 0 | 2.21 |
| 27 | 687 | 87.2 | 5 | 3.6 |
| 28 | 428 | 77.2 | 11 | 3.09 |
| 29 | 512 | 91.4 | 0 | 2.64 |

**Pemeriksaan manual awal (S1-T09)**

| Hal. | Temuan |
|---|---|
| 19 | Garis titik-titik contoh penomoran bab terbaca sebagai deretan huruf acak (`QLD eee cece ...`). "BAB II" → `BAB IL`, "iii" → `iil`. Teks paragraf benar, termasuk salah ketik asli "dilletakkan". |
| 28 | Tabel lembar penilaian: urutan sel teracak, baris judul berlatar biru ("N3 Seminar dan atau Laporan") hilang, "Penyajian" → `Penygim`, "Tampilan" → `Tanpin`, "(N1)" → `(ND`. Perlu transkripsi manual. |
| 16 | Judul bab terbaca `BAB II` padahal urutannya BAB III (perlu dicek terhadap gambar). |

**Peta isi** (dari judul hasil OCR): hal. 1–3 pembuka, 4–12 BAB I, 13–15 BAB II prosedur, 16 BAB III penilaian, 17–26 BAB IV–V format laporan, 27–28 lampiran instrumen penilaian, 29 berita acara. Usulan penyaringan: [`docs/scrum/sprint-01/usulan_penyaringan.md`](../scrum/sprint-01/usulan_penyaringan.md).

## Sesi 3 — 26 Oktober 2026 (S1-T12: ekspor Word/PDF)

**Instalasi**: pandoc 3.12.1 via `winget install --id JohnMacFarlane.Pandoc --exact --scope user` → `%LOCALAPPDATA%\Pandoc\pandoc.exe`.

**Analisis template** `Lembar Validasi Sprint Planning 1.docx` (Word 365, di-ignore git karena memuat NIP/NIM):
- A4, margin 1134 twip (2 cm) semua sisi, header 708, footer 708. Font default Times New Roman 11 pt.
- Header: logo PNG (anchor kiri, `wrapThrough`), judul tebal 14 pt, sub-judul tebal 12 pt, judul penelitian miring 10,5 pt dengan garis bawah ganda.
- Footer: abu-abu `595959` 9 pt, "<label> | Halaman {PAGE}".
- Judul bagian: tebal 12 pt, garis bawah tunggal `404040`, spasi sebelum 12 pt, sesudah 6 pt. Paragraf rata kiri-kanan, spasi 1,15.
- Tabel: garis tunggal `808080`, margin sel 3/5 pt, baris judul tebal 10 pt rata tengah dan berulang, isi 10,5 pt. Tabel identitas dan tanda tangan tanpa garis.
- `settings.xml`: `compatibilityMode=15`.

**Implementasi**
- `scripts/export_docs.py`:
  - `--build-reference <template.docx>` → `docs/templates/reference.docx`: reference default pandoc + gaya di atas (Body Text, Compact, Heading 1–3, Block Text, Checklist, Table), header template dengan penanda `{{HEADER_TITLE}}`/`{{HEADER_SUBTITLE}}`, footer baru dengan `{{FOOTER_LABEL}}` + field PAGE, `sectPr` A4/2 cm, dan blok `<w:compat>` dari template (tanpa itu teks header menimpa logo).
  - Ekspor: `pandoc -f gfm -t docx --reference-doc ... --lua-filter docs/templates/pekael-docx.lua --columns 10000`, lalu penanda header/footer diganti sesuai jenis dokumen, tabel dilebarkan 100% (`tblW pct 5000`), tabel tanpa baris judul dan tabel tanda tangan dibuat tanpa garis.
  - `--pdf`: konversi lewat Microsoft Word (COM, `SaveAs` format 17).
  - `{{NIM_DEVELOPER}}`, `{{NIP_PRODUCT_OWNER}}` diisi dari `.env` (kosong → garis isian).
- `docs/templates/pekael-docx.lua`: hapus H1 pertama (judul pindah ke header), `##` → Heading 1 bernomor ("1. …"), level lain naik satu, link → teks, kode → teks biasa, `<br>` → baris baru, tabel dengan header kosong → tanpa header, baris di blockquote dan paragraf kotak centang tetap terpisah (gaya Checklist, rata kiri).
- Lembar validasi (Sprint 1 dan templat): garis isian `____` (terbaca sebagai garis pemisah di Markdown) diganti titik-titik, NIP/NIM diganti penanda.
- `.gitignore`: `docs/export/`, `/*.docx`, `~$*.docx`. `.env.example`: `NIM_DEVELOPER=`, `NIP_PRODUCT_OWNER=`.

**Verifikasi**
- `reference.docx` diperiksa tidak memuat NIP, NIM, nama, maupun metadata penulis template.
- PDF hasil ekspor dirender dan dibandingkan dengan template: header, footer, tabel, dan tanda tangan sesuai.
- `pytest` → **100 lulus, 0 gagal** (baru: `test_export_docs.py`, 10 test).
