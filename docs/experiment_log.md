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

### EXP-002 — Ukuran potongan, tumpang tindih, normalisasi, dan dimensi vektor

| | |
|---|---|
| Tanggal | 2026-10-30 |
| Sprint | 2 |
| Tujuan | Memilih parameter awal `CHUNK_SIZE`/`CHUNK_OVERLAP` (OD-03), memastikan manfaat normalisasi L2 (OD-12), dan memilih dimensi vektor (OD-02) |
| Konfigurasi | `gemini-embedding-001`, task type `RETRIEVAL_DOCUMENT`/`RETRIEVAL_QUERY`, FAISS `IndexFlatL2`, k = 4, halaman 4–16 (koreksi OCR aktif), splitter per halaman |
| Data uji | 30 contoh pertanyaan dalam cakupan dari `topik_pertanyaan.md` beserta halaman sumbernya, 8 pertanyaan di luar cakupan (L1–L5 PKL tetapi tidak ada di buku, N1–N3 non-PKL). Data pengembangan, bukan dataset Ragas |
| Prosedur | `scripts/run_chunk_experiment.py`: setiap potongan dan pertanyaan di-embed satu kali (cache), lalu dicari dengan FAISS. Hit@1/Hit@4 = halaman yang diharapkan muncul di peringkat 1 / 4 besar. MRR = rata-rata 1/peringkat. Jarak = L2 potongan teratas. Varian 3072 dimensi dijalankan terpisah pada 1000:150 |
| Hasil | Lihat tabel di bawah. 204 teks dikirim ke API (140 + 64). Dua penolakan sementara (429/503) di awal pulih otomatis setelah jeda 20 dan 40 detik |
| Kesimpulan | Perbedaan antarukuran hanya satu pertanyaan dari 30, tidak cukup untuk menyatakan satu ukuran lebih baik. Nilai awal spesifikasi 1000:150 dipertahankan untuk Sprint 3 dan dinilai ulang dengan kualitas jawaban (Sprint 3–5). Normalisasi tidak mengubah peringkat (norma vektor asli hampir seragam, sekitar 0,58), tetapi membuat skala jarak tetap (0–2) sehingga ambang relevansi lebih mudah ditafsirkan, maka dipertahankan. Dimensi 3072 hanya unggul satu pertanyaan pada Hit@1 dengan ukuran vektor 4 kali lipat, maka 768 dipakai |
| Keputusan terkait | D-25, D-26, OD-02, OD-03, OD-12 |

| Varian | Potongan | Hit@1 | Hit@4 | MRR | Jarak dalam cakupan (rata-rata / maks) | Jarak luar cakupan (rata-rata / min) |
|---|---|---|---|---|---|---|
| 500:50 | 49 | 0,83 | 0,97 | 0,900 | 0,429 / 0,503 | 0,606 / 0,497 |
| 800:100 | 33 | 0,83 | 0,97 | 0,900 | 0,436 / 0,564 | 0,607 / 0,495 |
| 1000:150 | 26 | 0,83 | 0,97 | 0,894 | 0,451 / 0,604 | 0,613 / 0,497 |
| 1500:200 | 18 | 0,87 | 0,97 | 0,917 | 0,454 / 0,604 | 0,613 / 0,497 |
| 1000:150 tanpa normalisasi | 26 | 0,83 | 0,97 | 0,894 | 0,155 / 0,206 | 0,210 / 0,170 |
| 1000:150, 3072 dimensi | 26 | 0,87 | 0,97 | 0,911 | 0,431 / 0,558 | 0,580 / 0,466 |

Catatan analisis:
- Satu-satunya pertanyaan yang tidak ditemukan di semua varian (no. 2, dasar hukum PKL) mengambil halaman 13, yang memang menyebut Permendikbud No. 3 Tahun 2020. Label halaman pada daftar topik kurang lengkap dan diperbaiki menjadi 4–5, 13 setelah percobaan. Hasil di atas tetap dilaporkan sesuai label saat percobaan dijalankan.
- Jarak potongan teratas (1000:150, dinormalisasi): pertanyaan non-PKL N1–N3 0,683–0,741, pertanyaan PKL yang tidak dijawab buku L1–L5 0,497–0,615, pertanyaan dalam cakupan maksimum 0,604 (no. 28, tabel nilai). Ambang jarak dapat memisahkan pertanyaan non-PKL, tetapi tidak cukup untuk pertanyaan PKL yang informasinya tidak ada di buku. Bahan kalibrasi ambang (OD-04) dan kebijakan prompt pada Sprint 3.
