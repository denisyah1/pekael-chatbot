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

### EXP-003 — Tingkat "berpikir" Gemini dan waktu jawab

| | |
|---|---|
| Tanggal | 2026-11-07 |
| Sprint | 3 |
| Tujuan | Melihat apakah mengurangi tingkat berpikir model mempercepat jawaban tanpa menurunkan ketepatan (terkait butir UAT "jawaban kurang dari 5 detik") |
| Konfigurasi | `gemini-3.5-flash-lite`, `temperature=0`, `SYSTEM_PROMPT` D-30, 4 potongan konteks per pertanyaan (diambil manual dari `chunks_1000_150.jsonl`) |
| Data uji | 3 pertanyaan: syarat SKS (jawaban ada), batas pendaftaran (jawaban tidak ada), nilai 74 (butuh dua bagian) |
| Prosedur | Setiap pertanyaan dikirim satu kali per pengaturan: bawaan, `reasoning_effort="minimal"`, `"low"`. `thinking_budget=0` juga dicoba |
| Hasil | Lihat tabel. `thinking_budget=0` ditolak (`400 INVALID_ARGUMENT`) |
| Kesimpulan | Ketiga pengaturan memberi jawaban yang benar. Waktu jawab bervariasi lebar (1,4–9,8 s) tanpa pola yang konsisten, sehingga tidak ada bukti bahwa pengaturan berpikir mempercepat jawaban. Pengaturan bawaan dipertahankan, `GEMINI_REASONING_EFFORT` disediakan untuk penyetelan. Satu pengukuran per sel belum cukup: waktu jawab diukur ulang dengan sampel lebih besar pada pipeline lengkap (Sprint 5) |
| Keputusan terkait | D-32 |

| Pengaturan | Syarat SKS | Batas pendaftaran | Nilai 74 |
|---|---|---|---|
| Bawaan | 3,80 s, benar | 9,75 s, ditolak | 9,61 s, benar |
| `minimal` | 6,58 s, benar | 7,04 s, ditolak | 1,38 s, benar |
| `low` | 5,94 s, benar | 7,52 s, ditolak | 7,01 s, benar |

### EXP-004 — Kalibrasi awal batas jarak relevansi

| | |
|---|---|
| Tanggal | 2026-11-08 |
| Sprint | 3 |
| Tujuan | Menetapkan nilai awal `RETRIEVAL_MAX_L2_DISTANCE` (OD-04) dan memeriksa penolakan pertanyaan di luar cakupan pada alur lengkap |
| Konfigurasi | Indeks `20261102T180419398924-565a9929` (halaman 4–16, 22–25, 27–28, 33 potongan, 1000:150, 768 dimensi, dinormalisasi), `RETRIEVAL_K=4`, `gemini-3.5-flash-lite`, prompt D-30 + D-35 |
| Data uji | 30 pertanyaan dalam cakupan dan 8 di luar cakupan dari `topik_pertanyaan.md`, ditambah 6 pertanyaan dalam cakupan untuk halaman 22–28 (E1–E6 di `scripts/run_threshold_experiment.py`). Data pengembangan, bukan dataset Ragas |
| Prosedur | Aturan ditetapkan sebelum percobaan: ambang = titik tengah antara jarak potongan teratas terbesar pada pertanyaan dalam cakupan dan terkecil pada pertanyaan non-PKL (N1–N3), dibulatkan dua desimal. Pertanyaan L1–L5 tidak diharapkan terpisah oleh jarak (EXP-002), sehingga diperiksa lewat alur lengkap. `run_threshold_experiment.py --generate` menjalankan semua 44 pertanyaan melalui alur lengkap dengan ambang tersebut |
| Hasil | Hit@4 36/36. Jarak terbesar dalam cakupan 0,604 (no. 28), terkecil non-PKL 0,683 (N1), ambang 0,64. Jarak L1–L5 0,497–0,599, bercampur dengan pertanyaan dalam cakupan. Lihat tabel |
| Kesimpulan | Ambang 0,64 menolak semua pertanyaan non-PKL tanpa memanggil Gemini dan tidak menolak pertanyaan dalam cakupan. Pertanyaan PKL yang tidak dijawab buku seluruhnya ditolak oleh prompt. Satu *false negative*: no. 22 ("tahapan setelah diterima di tempat PKL") ditolak Gemini walaupun halaman 14 (prosedur pelaksanaan) terambil di peringkat 3. Satu jawaban kurang lengkap: E6 (cara menghitung nilai akhir) tidak memuat rumus 30/40/30 karena halaman 28 tidak masuk 4 besar. Waktu jawab median 1,65 s, 5 dari 36 pertanyaan dalam cakupan di atas 5 s (maks 13,10 s). Jarak non-PKL dan dalam cakupan hanya berselisih 0,08, sehingga ambang diuji ulang dengan pertanyaan baru pada Sprint 5 |
| Keputusan terkait | D-34, OD-04 |

| Kelompok | Jumlah | Jarak teratas (min–maks) | Ditolak ambang | Hasil alur lengkap | Waktu (median / maks) |
|---|---|---|---|---|---|
| Dalam cakupan | 36 | 0,296–0,604 | 0 | 35 dijawab, 1 ditolak (no. 22) | 1,76 / 13,10 s |
| PKL, tidak ada di buku (L) | 5 | 0,497–0,599 | 0 | 5 ditolak oleh prompt | 1,16 / 2,16 s |
| Non-PKL (N) | 3 | 0,683–0,741 | 3 | 3 ditolak ambang | 0,50 / 0,51 s |

Jawaban lengkap: [`scrum/sprint-03/pemeriksaan_jawaban.md`](scrum/sprint-03/pemeriksaan_jawaban.md). Data mentah: `data/processed/Pedoman-PKL-2025/exp004.json` (di-ignore git).

### EXP-005 — Model `gemini-3.5-flash` sebagai pengganti `gemini-3.5-flash-lite`

| | |
|---|---|
| Tanggal | 2026-11-15 |
| Sprint | 4 |
| Tujuan | Memeriksa apakah `gemini-3.5-flash` layak menggantikan `gemini-3.5-flash-lite` yang sedang lambat (OD-01) |
| Konfigurasi | Sama dengan EXP-004 (indeks 33 potongan, `RETRIEVAL_K=4`, ambang 0,64, prompt D-30 + D-35), hanya `GEMINI_CHAT_MODEL=gemini-3.5-flash`, `GEMINI_TIMEOUT_SECONDS=30` |
| Data uji | 44 pertanyaan EXP-004 |
| Prosedur | `run_threshold_experiment.py --generate --pause 6 --output .../exp005.json`, jeda 6 detik antarpanggilan |
| Hasil | 13 dari 36 pertanyaan dalam cakupan dijawab (4,0–28,1 s), 2 gagal setelah 9,8 dan 15,0 s, lalu semua permintaan berikutnya ditolak dalam ±1 s. Pesan server: `429 RESOURCE_EXHAUSTED`, `GenerateRequestsPerDayPerProjectPerModel-FreeTier`, batas 20 permintaan per hari. Pertanyaan non-PKL tetap ditolak ambang tanpa memanggil Gemini. `gemini-3.5-flash-lite` pada saat yang sama menjawab dalam 18,95 s |
| Kesimpulan | Kuota gratis `gemini-3.5-flash` (20 permintaan per hari) tidak mencukupi pengujian maupun UAT, dan waktu jawab pada alur lengkap tidak lebih cepat. Model dikembalikan ke `gemini-3.5-flash-lite` |
| Keputusan terkait | D-40, OD-01 |
