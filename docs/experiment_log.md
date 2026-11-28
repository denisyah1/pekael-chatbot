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

### EXP-006 — Respons arahan untuk pertanyaan yang jawabannya tidak ada di buku

| | |
|---|---|
| Tanggal | 2026-11-17 |
| Sprint | 4 |
| Tujuan | Memeriksa respons arahan pengganti teks fallback (D-45): ramah, bervariasi, mengarahkan ke pihak yang tepat, tanpa menebak, dan tanpa mengubah jawaban dalam cakupan |
| Konfigurasi | Indeks `20261104T043244948591-565a9929`, `RETRIEVAL_K=4`, ambang 0,64, `gemini-3.5-flash-lite`, prompt D-30 + D-35 + D-45 |
| Data uji | L1–L5 dan N1–N3 dari `topik_pertanyaan.md`, 1 pertanyaan baru (kerja paruh waktu selama PKL), 5 pertanyaan dalam cakupan |
| Prosedur | Dua putaran `scripts/ask.py`. Prompt diperketat di antara putaran berdasarkan temuan putaran pertama |
| Hasil | Putaran 1: 2 dari 5 arahan masih memakai "tidak tersedia" dan "belum tercantum", sapaan bercampur. Putaran 2: 5 dari 5 arahan tanpa ungkapan terlarang, sapaan "kamu", pihak yang dituju sesuai topik. N1–N3 memakai kalimat siap pakai. Jawaban dalam cakupan tetap sama dengan rujukan yang sama |
| Kesimpulan | Respons arahan memenuhi permintaan PO pada contoh yang diuji. Jumlah contoh kecil, sehingga respons arahan ikut diperiksa pada pengujian Sprint 5 |
| Keputusan terkait | D-45 |

### EXP-007 — Gaya jawaban adaptif dan ketepatan jawaban

| | |
|---|---|
| Tanggal | 2026-11-18 |
| Sprint | 4 |
| Tujuan | Memastikan gaya jawaban baru (D-46) dan perubahan ambang (D-47) tidak menurunkan ketepatan dibanding EXP-004 |
| Konfigurasi | Indeks `20261104T043244948591-565a9929`, `RETRIEVAL_K=4`, ambang 0,64 (hanya memutuskan), `gemini-3.5-flash-lite`, prompt D-30 + D-45 + D-46 |
| Data uji | 44 pertanyaan EXP-004 |
| Prosedur | `run_threshold_experiment.py --generate --pause 4 --output .../exp007.json`, dibandingkan dengan `exp004.json` |
| Hasil | Dalam cakupan 36/36 dijawab (EXP-004: 35/36). Pertanyaan no. 22 kini dijawab dengan urutan prosedur halaman 14. L1–L5 5/5 diarahkan, N1–N3 3/3 dibalas sebagai percakapan. Tidak ada ungkapan terlarang atau penanda yang tampil. Waktu jawab dalam cakupan median 2,77 s, maks 9,95 s, 7 dari 36 di atas 5 s. Balasan percakapan N1–N3 median 8,63 s. E6 (cara menghitung nilai akhir) masih belum memuat rumus 30/40/30 halaman 28 |
| Kesimpulan | Ketepatan tidak turun, cakupan naik satu pertanyaan. Waktu jawab naik sekitar 1 s karena prompt dan jawaban lebih panjang. Balasan percakapan perlu dipantau |
| Keputusan terkait | D-46, D-47 |

### EXP-008 — Penyebab waktu jawab yang lebih lama

| | |
|---|---|
| Tanggal | 2026-11-19 |
| Sprint | 4 |
| Tujuan | Memeriksa apakah instruksi yang lebih panjang (D-46) atau tingkat berpikir Gemini memperlambat jawaban |
| Konfigurasi | `gemini-3.5-flash-lite`, `timeout=40`, konteks 4 potongan yang sama per pertanyaan, koneksi dipanaskan lebih dulu |
| Data uji | 6 pertanyaan (definisi PKL dalam tiga gaya, nilai 74, dokumen lampiran, SKS minimal), masing-masing 2 putaran |
| Prosedur | Perbandingan 1: `reasoning_effort` bawaan dan `minimal` dengan instruksi sekarang. Perbandingan 2: instruksi commit `a9616d0` (933 karakter) dan instruksi sekarang (3.335 karakter). Setiap pasangan dijalankan bergantian pada waktu yang sama |
| Hasil | Bawaan median 8,03 s, `minimal` 8,65 s. Instruksi lama 7,21 s (n=11), instruksi baru 7,04 s. Panjang jawaban median 332–444 karakter |
| Kesimpulan | Panjang instruksi dan tingkat berpikir tidak menjelaskan perlambatan. Pada hari sebelumnya instruksi yang sama memerlukan median 2,77 s (EXP-007), sehingga perbedaan berasal dari kondisi layanan. Pengaturan bawaan dipertahankan |
| Keputusan terkait | D-32, D-48 |

### EXP-009 — Ketepatan setelah perbaikan petunjuk arahan

| | |
|---|---|
| Tanggal | 2026-11-19 |
| Sprint | 4 |
| Tujuan | Memastikan pertanyaan yang ada jawabannya kembali dijawab setelah petunjuk bentuk arahan dipindah (D-50) |
| Konfigurasi | Seperti EXP-007, ditambah bentuk penyajian acak (D-49) dan perbaikan D-50 |
| Data uji | 44 pertanyaan EXP-004 |
| Prosedur | `run_threshold_experiment.py --generate --pause 4 --output .../exp009.json`, dibandingkan dengan `exp007.json` |
| Hasil | Dalam cakupan 35/36 dijawab. No. 23 (pembekalan sebelum PKL) diarahkan ke Admin Prodi PTIK, pada EXP-007 dijawab. L1–L5 5/5 diarahkan, N1–N3 3/3 dibalas sebagai percakapan. Tidak ada penanda, ungkapan terlarang, atau sapaan pembuka yang tidak diminta. Satu arahan memuat "belum ada di panduan kita", frasa ini ditambahkan ke daftar ungkapan yang dicegah. Waktu jawab dalam cakupan median 5,44 s, maks 7,73 s |
| Kesimpulan | Ketepatan kembali setara EXP-004 sampai EXP-007. Satu pertanyaan berubah status antar percobaan, sehingga hasil perlu diukur dengan beberapa kali pengulangan pada evaluasi Sprint 5. Waktu jawab mengikuti kondisi layanan |
| Keputusan terkait | D-49, D-50 |

### EXP-010 — Ketepatan setelah dokumen knowledge base tambahan

| | |
|---|---|
| Tanggal | 2026-11-20 |
| Sprint | 5 |
| Tujuan | Memeriksa pengaruh dokumen knowledge base tambahan dari *Product Owner* (D-53) terhadap jarak kedekatan, ketepatan, dan waktu jawab |
| Konfigurasi | Indeks `20261124T053813125686-565a9929` (Buku Pedoman 33 potongan, dokumen tambahan 28 potongan), `RETRIEVAL_K=4`, ambang tetap 0,64, `gemini-3.5-flash-lite`, prompt EXP-009 dengan label nama dokumen |
| Data uji | 44 pertanyaan EXP-004 |
| Prosedur | `run_threshold_experiment.py --generate --pause 4 --threshold 0.64 --output .../exp010.json`, dibandingkan dengan `exp009.json` |
| Hasil | Dalam cakupan 36/36 dijawab (EXP-009: 35/36). E6 kini memuat rumus nilai akhir 30% N1 + 40% N2 + 30% N3 dari dokumen tambahan. Dari kelompok L, L5 (margin dan huruf laporan) dan L2 (jadwal pembekalan) dijawab dari dokumen tambahan, L1, L3, L4 diarahkan. N1–N3 3/3 ditolak ambang. Jarak terbesar dalam cakupan 0,557, terkecil non-PKL 0,663 (titik tengah 0,61), jarak N1 hanya 0,023 di atas ambang 0,64. Halaman Buku Pedoman yang diharapkan terambil pada 34/36 pertanyaan, dua lainnya dijawab dari dokumen tambahan. Waktu jawab median 1,68 s, maks 2,35 s |
| Kesimpulan | Dokumen tambahan menambah cakupan tanpa menurunkan ketepatan. Kelompok L tidak lagi seluruhnya di luar cakupan sehingga perlu disusun ulang untuk dataset Sprint 5. Ambang 0,64 masih memisahkan, tetapi selisih dengan pertanyaan non-PKL terdekat mengecil dan perlu diuji ulang sebelum dibekukan (S5-T07). Jawaban L2 memakai kalimat tentang jadwal seminar dan perlu diperiksa *Product Owner*. Pada uji langsung L4 dijawab dengan nama Koordinator PKL, sehingga statusnya masih berubah antar percobaan |
| Keputusan terkait | D-53, D-54 |

### EXP-011 — Ketepatan setelah perbaikan pemeriksaan arahan

| | |
|---|---|
| Tanggal | 2026-11-21 |
| Sprint | 5 |
| Tujuan | Memastikan perbaikan D-55 tidak membuat pertanyaan yang memang tidak ada jawabannya lolos sebagai jawaban |
| Konfigurasi | Seperti EXP-010, ditambah perbaikan D-54 lanjutan dan D-55 |
| Data uji | 44 pertanyaan EXP-004 |
| Prosedur | `run_threshold_experiment.py --generate --pause 4 --threshold 0.64 --output .../exp011.json`, dibandingkan dengan `exp010.json` |
| Hasil | Dalam cakupan 36/36 dijawab. L4 (Koordinator PKL) dan L5 (margin dan huruf laporan) dijawab dari dokumen tambahan. L1, L2, L3 diarahkan, L2 (jadwal pembekalan) tidak lagi memakai kalimat jadwal seminar. N1–N3 3/3 ditolak ambang. Tidak ada sapaan pembuka atau penanda yang tampil. Waktu jawab median 1,67 s, maks 9,28 s (satu pertanyaan), lainnya di bawah 2,5 s |
| Kesimpulan | Perbaikan tidak menurunkan ketepatan. Dari kelompok L, dua pertanyaan kini termasuk cakupan dokumen tambahan, sehingga kelompok pertanyaan tidak tercakup perlu disusun ulang pada dataset Sprint 5 |
| Keputusan terkait | D-54, D-55 |

### EXP-012 — Uji coba Ragas pada 36 pertanyaan uji

| | |
|---|---|
| Tanggal | 2026-11-25 |
| Sprint | 5 |
| Tujuan | Memastikan ketiga metrik Ragas berjalan dari jawaban Pekael sampai nilai per pertanyaan, dan mengetahui kebutuhan kuota evaluator (S5-T08) |
| Konfigurasi | Indeks `20261124T053813125686-565a9929`, `gemini-3.5-flash-lite`, `k=4`, ambang 0,64, evaluator `openai/gpt-oss-120b` (Groq, `max_tokens=4096`), embedding `gemini-embedding-001`, Ragas 0.4.3 |
| Data uji | Dataset v2 scope `uji36` (36 pertanyaan), belum divalidasi *Product Owner* |
| Prosedur | `run_ragas_evaluation.py --experiment EXP-012 --scope uji36 --pause 20`, hasil di `data/evaluation/results/EXP-012/` |
| Hasil | 36/36 dijawab Pekael (median 1,79 s). 18/36 dinilai sebelum batas token harian Groq tercapai. Rerata 18 pertanyaan: Faithfulness 0,901, Answer Relevancy 0,906, Context Recall 0,972. Nilai terendah: Faithfulness no. 15 (0,333, salah tafsir evaluator) dan no. 14 (0,500, kalimat basa-basi), Context Recall no. 2 (0,500, halaman dasar hukum tidak terambil) |
| Kesimpulan | Integrasi ketiga metrik berhasil dan setiap nilai dapat ditelusuri. Kalimat pengantar dan penutup yang ramah menurunkan Faithfulness, penilai dapat salah tafsir sehingga nilai rendah perlu diperiksa manual, dan pencarian belum menemukan halaman dasar hukum. Kuota gratis cukup untuk sekitar 21 pertanyaan per hari. Hasil ini uji coba, bukan hasil penelitian |
| Keputusan terkait | D-52, D-57, D-58 |
