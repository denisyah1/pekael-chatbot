# Lembar Validasi Sprint Report 4 — Bagian A: Sprint Planning

| | |
|---|---|
| Sprint | : Sprint 4 |
| Periode Sprint | : 13 – 26 November 2026 |
| *Product Owner* (validator) | : Dosen Koordinator PKL Prodi PTIK UNJ |
| Scrum Master | : Dosen pembimbing |
| Developer | : Deni Merdiansyah (NIM {{NIM_DEVELOPER}}) |

## Tujuan

Lembar ini memuat hasil *Sprint Planning* Sprint 4 untuk divalidasi oleh *Product Owner* dari sisi kebutuhan informasi PKL dan urutan pengerjaan, sebelum Sprint 4 dikerjakan. Sesuai Scrum Guide, *Sprint backlog* terdiri atas *Sprint Goal*, Product Backlog Item yang dipilih untuk Sprint, dan rencana pengerjaannya, ketiganya disajikan pada bagian 2 sampai 4.

## *Sprint Goal*

Menghasilkan website Pekael yang dapat dipakai secara lokal: mahasiswa dapat mengetik pertanyaan dan menerima jawaban beserta rujukan halaman buku panduan melalui tampilan yang sederhana dan mudah dipahami, admin dapat masuk dengan satu akun lalu memperbarui buku panduan tanpa menghilangkan knowledge base yang sedang dipakai, dan seluruh fungsi diuji sebelum validasi ahli pada Sprint 5.

## Product Backlog Item yang dipilih

| No | Product Backlog Item | Prioritas | Alasan dipilih pada Sprint 4 |
|---|---|---|---|
| 1 | Antarmuka website untuk tanya-jawab | Tinggi | Alur tanya-jawab dari Sprint 3 perlu dapat dipakai mahasiswa tanpa perintah terminal |
| 2 | Penampilan rujukan sumber pada setiap jawaban | Sedang | Rujukan halaman sudah tersedia dari alur tanya-jawab dan perlu ditampilkan dengan jelas |
| 3 | Admin mengunggah/memperbarui dokumen knowledge base | Sedang | Buku panduan dapat berganti versi, sehingga pembaruan perlu dilakukan tanpa bantuan Developer |

## Rencana pengerjaan (*Sprint backlog*)

| | |
|---|---|
| Masukan | : Alur tanya-jawab dan knowledge base hasil Sprint 3, batas kedekatan awal 0,64 |
| Alat | : Streamlit, LangChain, FAISS, model Gemini `gemini-3.5-flash-lite` |
| Prinsip tampilan | : Sederhana, bahasa yang wajar untuk layanan akademik, tanpa kesan "robot", teks mudah dibaca, dapat dipakai di laptop dan ponsel |

| No | Tugas | PBI terkait | Keluaran | Waktu |
|---|---|---|---|---|
| 1 | Memeriksa ulang label halaman daftar topik pertanyaan dan menambah contoh pertanyaan untuk halaman 22–28 (rencana perbaikan Sprint 3) | 1 | Daftar topik yang diperbarui | 13 November 2026 |
| 2 | Merancang dan membuat halaman tanya-jawab mahasiswa: kolom pertanyaan, tanda proses, jawaban, dan pesan gangguan | 1 | Tampilan pertama halaman mahasiswa | 13 – 15 November 2026 |
| 3 | Menampilkan rujukan nama dokumen, halaman PDF, bagian, dan kutipan singkat | 2 | Rujukan pada setiap jawaban | 13 – 15 November 2026 |
| 4 | Evaluasi tampilan pertama oleh Developer dan perbaikannya | 1, 2 | Tampilan yang disepakati | 16 – 17 November 2026 |
| 5 | Login satu akun admin dari pengaturan, tanpa pendaftaran akun | 3 | Halaman login admin | 18 – 19 November 2026 |
| 6 | Halaman admin untuk mengunggah atau mengganti buku panduan beserta laporan pembangunan knowledge base | 3 | Pembaruan knowledge base dari website | 19 – 21 November 2026 |
| 7 | Pembatasan panjang pertanyaan dan pencegahan pengiriman berulang | 1 | Pengaman penggunaan layanan | 22 November 2026 |
| 8 | Pengujian otomatis tampilan dan uji seluruh penggunaan mahasiswa dan admin dari website, termasuk waktu jawab | 1, 2, 3 | Hasil pengujian internal | 23 – 25 November 2026 |

## Increment dan kriteria selesai

| Increment | Kriteria selesai | Titik validasi |
|---|---|---|
| Halaman tanya-jawab mahasiswa | Pertanyaan dapat dikirim, tanda proses tampil, jawaban tampil bersama nama dokumen dan halaman PDF dari potongan yang benar-benar diambil, pertanyaan di luar cakupan dan gangguan layanan menampilkan pesan yang jelas, tampilan dapat dipakai di laptop dan ponsel | Developer mengevaluasi tampilan, dikonfirmasi *Product Owner* pada *Sprint Review* |
| Halaman admin | Hanya satu akun admin dari pengaturan yang dapat masuk, admin dapat mengganti buku panduan, laporan pembangunan tampil, dan knowledge base lama tetap dipakai bila pembangunan gagal | Peneliti memeriksa, dikonfirmasi pada *Sprint Review* |

## Peran dan keterlibatan pada Sprint 4

| Peran | Pemegang | Keterlibatan | Keluaran |
|---|---|---|---|
| *Product Owner* | Dosen koordinator PKL | Memvalidasi kebutuhan dan urutan pada *Sprint Planning*, mencoba website pada *Sprint Review* | Bukti validasi |
| Scrum Master | Dosen pembimbing | Memastikan *Sprint Planning*, *Sprint Review*, dan *Sprint Retrospective* terlaksana, mengonfirmasi checklist akhir Sprint | Konfirmasi checklist |
| Developers | Peneliti | Mengerjakan *Sprint backlog*, mengevaluasi tampilan, dan mengisi logbook setiap hari kerja aktif | Logbook, Increment |

## Jadwal peristiwa Sprint 4

| Peristiwa | Waktu | Pelaksana |
|---|---|---|
| *Sprint Planning* | 13 November 2026 | Peneliti, *Product Owner* |
| Pengerjaan harian (logbook) | 13 – 26 November 2026 | Peneliti |
| Evaluasi tampilan pertama | 16 November 2026 | Peneliti |
| *Sprint Review* | 26 November 2026 | Peneliti, *Product Owner*, Scrum Master |
| *Sprint Retrospective* | 26 November 2026 | Peneliti, Scrum Master |

## Risiko dan penanganan

| Risiko | Dampak | Penanganan |
|---|---|---|
| Tampilan terasa kaku atau membingungkan bagi mahasiswa nonteknis | Mahasiswa enggan memakai Pekael | Tampilan dibuat sederhana dengan bahasa yang wajar, dievaluasi Developer sebelum dilanjutkan |
| Waktu jawab kadang lebih dari 5 detik | Mahasiswa mengira website tidak bekerja | Tanda proses selalu tampil, waktu jawab dicatat pada setiap uji |
| Buku panduan baru yang diunggah admin hasil scan tanpa koreksi OCR | Isi knowledge base kurang akurat | Laporan pembangunan menampilkan halaman OCR yang belum diperiksa |
| Kata sandi admin bocor ke repository | Akun admin dapat disalahgunakan | Kata sandi hanya dibaca dari pengaturan lokal, pemeriksa API key aktif sebelum setiap penyimpanan perubahan |

## Pernyataan validasi

Berdasarkan kebutuhan informasi PKL di Prodi PTIK, *Sprint Planning* Sprint 4 pada lembar ini, yaitu *Sprint Goal*, *Product Backlog Item* yang dipilih, rencana pengerjaan, serta Increment yang diharapkan, telah divalidasi dan dapat dilaksanakan.

| | |
|---|---|
| Jakarta, 13 November 2026<br>*Product Owner* (Dosen Koordinator PKL),<br><br><br><br>Bambang Satrio, S. Pd., M. Kom.<br>NIP. {{NIP_PRODUCT_OWNER}} | <br>Developer,<br><br><br><br>Deni Merdiansyah<br>NIM {{NIM_DEVELOPER}} |

*Dasar penyusunan: Schwaber & Sutherland (2020) untuk komponen Sprint Planning, Liu et al. (2019) dan Verwijs & Russo (2023) untuk peran perencanaan Sprint yang jelas dan umpan balik pemangku kepentingan. Rujukan lengkap tercantum pada laporan.*
