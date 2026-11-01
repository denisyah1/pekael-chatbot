# Lembar Validasi Sprint Report 3 — Bagian A: Sprint Planning

| | |
|---|---|
| Sprint | : Sprint 3 |
| Periode Sprint | : 6 – 12 November 2026 |
| *Product Owner* (validator) | : Dosen Koordinator PKL Prodi PTIK UNJ |
| Scrum Master | : Dosen pembimbing |
| Developer | : Deni Merdiansyah (NIM {{NIM_DEVELOPER}}) |

## Tujuan

Lembar ini memuat hasil *Sprint Planning* Sprint 3 untuk divalidasi oleh *Product Owner* dari sisi kebutuhan informasi PKL dan urutan pengerjaan, sebelum Sprint 3 dikerjakan. Sesuai Scrum Guide, *Sprint backlog* terdiri atas *Sprint Goal*, Product Backlog Item yang dipilih untuk Sprint, dan rencana pengerjaannya, ketiganya disajikan pada bagian 2 sampai 4.

## *Sprint Goal*

Menghasilkan alur tanya-jawab Pekael yang berjalan lengkap tanpa antarmuka: knowledge base tersimpan di FAISS dan dapat dimuat ulang, pertanyaan dicarikan potongan teks yang relevan, Gemini menyusun jawaban hanya dari potongan tersebut beserta rujukan halaman, dan pertanyaan di luar cakupan dijawab dengan pesan penolakan, sebagai dasar antarmuka Streamlit pada Sprint 4.

## Product Backlog Item yang dipilih

| No | Product Backlog Item | Prioritas | Alasan dipilih pada Sprint 3 |
|---|---|---|---|
| 1 | Penyimpanan embedding pada FAISS | Tinggi | Vektor dari Sprint 2 perlu disimpan dan dapat dimuat ulang agar knowledge base tidak dibangun setiap kali aplikasi berjalan |
| 2 | Retrieval chain menghubungkan FAISS dan Gemini API | Tinggi | Inti layanan tanya-jawab yang akan dipakai antarmuka pada Sprint 4 |
| 3 | Ekstraksi teks melalui OCR (lanjutan untuk halaman tambahan) | Tinggi | Halaman 22–25 dan 27–28 yang ditetapkan *Product Owner* perlu diperiksa sebelum masuk knowledge base |

## Rencana pengerjaan (*Sprint backlog*)

| | |
|---|---|
| Masukan | : Potongan teks dan model embedding hasil Sprint 2, keputusan halaman knowledge base (4–16, 22–25, 27–28) |
| Alat | : FAISS `IndexFlatL2`, LangChain, model Gemini `gemini-3.5-flash-lite` |
| Parameter awal | : Potongan 1.000 karakter dengan tumpang tindih 150, ukuran vektor 768, 4 potongan diambil per pertanyaan |

| No | Tugas | PBI terkait | Keluaran | Waktu |
|---|---|---|---|---|
| 1 | Memeriksa dan mengoreksi OCR halaman 22–25 dan 27–28, termasuk menulis ulang tabel halaman 27–28 (bawaan Sprint 2) | 3 | Teks halaman tambahan terverifikasi | 6 – 7 November 2026 |
| 2 | Menyimpan knowledge base ke FAISS: membangun, menyimpan berversi, dan memuat ulang | 1 | Indeks FAISS yang dapat dimuat ulang | 6 – 7 November 2026 |
| 3 | Menghubungkan model Gemini untuk menyusun jawaban, termasuk penanganan gangguan layanan | 2 | Penghubung model Gemini | 8 November 2026 |
| 4 | Menyusun alur tanya-jawab yang berurutan: periksa pertanyaan, cari potongan, periksa relevansi, susun konteks, minta jawaban, periksa rujukan | 2 | Alur tanya-jawab beserta instruksi untuk Gemini | 8 – 9 November 2026 |
| 5 | Merakit seluruh komponen dan menyediakan perintah untuk membangun knowledge base dan bertanya dari terminal | 1, 2 | Alur dapat dijalankan dari awal sampai akhir | 9 – 10 November 2026 |
| 6 | Kalibrasi awal batas relevansi dengan pertanyaan dalam dan luar cakupan | 2 | Nilai batas awal dan catatan percobaan | 10 – 11 November 2026 |
| 7 | Menguji kondisi gagal: knowledge base belum dibangun, API key salah, kuota habis, layanan lambat, dan hasil pencarian kosong | 2 | Hasil uji kondisi gagal | 11 – 12 November 2026 |

## Increment dan kriteria selesai

| Increment | Kriteria selesai | Titik validasi |
|---|---|---|
| Knowledge base tersimpan di FAISS | Indeks dibangun dari halaman yang disetujui, dapat dimuat ulang pada proses baru, dan pembangunan yang gagal tidak mengganti indeks yang sedang dipakai | Peneliti memeriksa, dikonfirmasi pada *Sprint Review* |
| Alur tanya-jawab tanpa antarmuka | Pertanyaan dalam cakupan dijawab berdasarkan buku panduan beserta rujukan halaman yang benar-benar diambil, pertanyaan di luar cakupan dijawab dengan pesan penolakan, gangguan layanan menampilkan pesan yang jelas | Contoh tanya-jawab diperiksa *Product Owner* pada *Sprint Review* |

## Peran dan keterlibatan pada Sprint 3

| Peran | Pemegang | Keterlibatan | Keluaran |
|---|---|---|---|
| *Product Owner* | Dosen koordinator PKL | Memvalidasi kebutuhan dan urutan pada *Sprint Planning*, memeriksa contoh jawaban chatbot pada *Sprint Review* | Bukti validasi |
| Scrum Master | Dosen pembimbing | Memastikan *Sprint Planning*, *Sprint Review*, dan *Sprint Retrospective* terlaksana, mengonfirmasi checklist akhir Sprint | Konfirmasi checklist |
| Developers | Peneliti | Mengerjakan *Sprint backlog* dan mengisi logbook setiap hari kerja aktif | Logbook, Increment |

## Jadwal peristiwa Sprint 3

| Peristiwa | Waktu | Pelaksana |
|---|---|---|
| *Sprint Planning* | 6 November 2026 | Peneliti, *Product Owner* |
| Pengerjaan harian (logbook) | 6 – 12 November 2026 | Peneliti |
| Pemeriksaan contoh jawaban bersama *Product Owner* | 10 November 2026 | Peneliti, *Product Owner* |
| *Sprint Review* | 12 November 2026 | Peneliti, *Product Owner*, Scrum Master |
| *Sprint Retrospective* | 12 November 2026 | Peneliti, Scrum Master |

## Risiko dan penanganan

| Risiko | Dampak | Penanganan |
|---|---|---|
| Gemini menyusun jawaban di luar isi buku panduan | Mahasiswa menerima informasi keliru | Instruksi yang membatasi jawaban pada konteks, rujukan diambil dari potongan yang benar-benar dipakai, contoh jawaban diperiksa *Product Owner* |
| Pertanyaan PKL yang jawabannya tidak ada di buku sulit ditolak lewat pencarian | Chatbot menebak jawaban | Instruksi kepada Gemini untuk menyatakan informasi tidak ditemukan, diuji dengan pertanyaan di luar cakupan |
| Layanan Gemini sibuk atau kuota gratis habis | Jawaban gagal atau lambat | Pesan gangguan yang jelas, percobaan ulang terbatas, tanpa beralih ke layanan berbayar |
| Waktu jawab lebih dari 5 detik | Tidak memenuhi harapan pada kuesioner UAT | Waktu jawab mulai dicatat pada setiap uji coba |

## Pernyataan validasi

Berdasarkan kebutuhan informasi PKL di Prodi PTIK, *Sprint Planning* Sprint 3 pada lembar ini, yaitu *Sprint Goal*, *Product Backlog Item* yang dipilih, rencana pengerjaan, serta Increment yang diharapkan, telah divalidasi dan dapat dilaksanakan.

| | |
|---|---|
| Jakarta, 6 November 2026<br>*Product Owner* (Dosen Koordinator PKL),<br><br><br><br>Bambang Satrio, S. Pd., M. Kom.<br>NIP. {{NIP_PRODUCT_OWNER}} | <br>Developer,<br><br><br><br>Deni Merdiansyah<br>NIM {{NIM_DEVELOPER}} |

*Dasar penyusunan: Schwaber & Sutherland (2020) untuk komponen Sprint Planning, Liu et al. (2019) dan Verwijs & Russo (2023) untuk peran perencanaan Sprint yang jelas dan umpan balik pemangku kepentingan. Rujukan lengkap tercantum pada laporan.*
