# Lembar Validasi Sprint Report 2 — Bagian A: Sprint Planning

| | |
|---|---|
| Sprint | : Sprint 2 |
| Periode Sprint | : 30 Oktober – 6 November 2026 |
| *Product Owner* (validator) | : Dosen Koordinator PKL Prodi PTIK UNJ |
| Scrum Master | : Dosen pembimbing |
| Developer | : Deni Merdiansyah (NIM {{NIM_DEVELOPER}}) |

## Tujuan

Lembar ini memuat hasil *Sprint Planning* Sprint 2 untuk divalidasi oleh *Product Owner* dari sisi kebutuhan informasi PKL dan urutan pengerjaan, sebelum Sprint 2 dikerjakan. Sesuai Scrum Guide, *Sprint backlog* terdiri atas *Sprint Goal*, Product Backlog Item yang dipilih untuk Sprint, dan rencana pengerjaannya, ketiganya disajikan pada bagian 2 sampai 4.

## *Sprint Goal*

Mengubah teks buku panduan PKL yang telah disaring menjadi potongan teks (*chunk*) yang tetap membawa keterangan sumber dan halaman, lalu menjadi representasi vektor menggunakan model embedding Gemini, dengan ukuran potongan awal yang dipilih berdasarkan percobaan, sebagai dasar penyimpanan FAISS dan alur tanya-jawab pada Sprint 3.

## Product Backlog Item yang dipilih

| No | Product Backlog Item | Prioritas | Alasan dipilih pada Sprint 2 |
|---|---|---|---|
| 1 | Text splitting dan embedding menjadi representasi vektor | Tinggi | Tahap lanjutan dari teks hasil Sprint 1 dan prasyarat penyimpanan vektor pada Sprint 3 |
| 2 | Penyaringan dan pengerucutan konten sesuai lingkup Prodi PTIK (lanjutan Sprint 1) | Tinggi | Keputusan *Product Owner* atas halaman yang dipakai perlu diterapkan sebelum teks dipotong |

## Rencana pengerjaan (*Sprint backlog*)

| | |
|---|---|
| Masukan | : Teks per halaman Buku Pedoman PKL 2025 hasil Sprint 1 beserta koreksi manualnya |
| Alat | : LangChain RecursiveCharacterTextSplitter, model embedding Gemini `gemini-embedding-001` |
| Parameter awal | : Ukuran potongan 1.000 karakter, tumpang tindih 150 karakter, ukuran vektor 768 (nilai awal percobaan, bukan nilai final) |

| No | Tugas | PBI terkait | Keluaran | Waktu |
|---|---|---|---|---|
| 1 | Menyelesaikan bawaan Sprint 1: verifikasi akhir koreksi OCR dan keputusan *Product Owner* atas halaman yang dipakai | 2 | Teks terverifikasi dan daftar halaman knowledge base yang disetujui | 30 – 31 Oktober 2026 |
| 2 | Menerapkan pemilihan halaman knowledge base sesuai keputusan *Product Owner* | 2 | Hanya halaman yang disetujui yang diproses | 30 – 31 Oktober 2026 |
| 3 | Memotong teks menjadi *chunk* dengan keterangan sumber, halaman, dan bagian (judul bab/subbab) | 1 | Potongan teks berlabel sumber | 30 Oktober – 1 November 2026 |
| 4 | Mengintegrasikan model embedding Gemini untuk dokumen dan pertanyaan, termasuk penanganan batas kuota | 1 | Vektor dokumen dan pertanyaan dengan ukuran konsisten | 1 – 3 November 2026 |
| 5 | Percobaan ukuran potongan dan tumpang tindih memakai contoh pertanyaan dari daftar topik Sprint 1 | 1 | Catatan percobaan dan parameter awal terpilih | 3 – 5 November 2026 |
| 6 | Mencatat statistik potongan (jumlah, potongan kosong atau ganda) dan memeriksa konsistensi ukuran vektor | 1 | Laporan potongan dan vektor | 5 – 6 November 2026 |

## Increment dan kriteria selesai

| Increment | Kriteria selesai | Titik validasi |
|---|---|---|
| Potongan teks berlabel sumber | Setiap potongan menyimpan nama dokumen, halaman PDF, bagian, dan nomor unik, hanya berasal dari halaman yang disetujui *Product Owner* | Peneliti memeriksa, dikonfirmasi pada *Sprint Review* |
| Vektor embedding dan parameter awal | Semua potongan dan pertanyaan menghasilkan vektor berukuran sama, percobaan ukuran potongan tercatat beserta alasan pemilihan parameter awal | Catatan percobaan diperiksa pada *Sprint Review* |

## Peran dan keterlibatan pada Sprint 2

| Peran | Pemegang | Keterlibatan | Keluaran |
|---|---|---|---|
| *Product Owner* | Dosen koordinator PKL | Memutuskan halaman buku panduan yang dipakai, memvalidasi isi Increment pada *Sprint Review* | Keputusan penyaringan, bukti validasi |
| Scrum Master | Dosen pembimbing | Memastikan *Sprint Planning*, *Sprint Review*, dan *Sprint Retrospective* terlaksana, mengonfirmasi checklist akhir Sprint | Konfirmasi checklist |
| Developers | Peneliti | Mengerjakan *Sprint backlog* dan mengisi logbook setiap hari kerja aktif | Logbook, Increment |

## Jadwal peristiwa Sprint 2

| Peristiwa | Waktu | Pelaksana |
|---|---|---|
| *Sprint Planning* | 30 Oktober 2026 | Peneliti, *Product Owner* |
| Keputusan penyaringan halaman | 31 Oktober 2026 | Peneliti, *Product Owner* |
| Pengerjaan harian (logbook) | 30 Oktober – 6 November 2026 | Peneliti |
| *Sprint Review* | 6 November 2026 | Peneliti, *Product Owner*, Scrum Master |
| *Sprint Retrospective* | 6 November 2026 | Peneliti, Scrum Master |

## Risiko dan penanganan

| Risiko | Dampak | Penanganan |
|---|---|---|
| Kuota gratis layanan Gemini terbatas | Pembuatan vektor terhenti di tengah proses | Permintaan dikirim berkelompok, jeda dan percobaan ulang terbatas saat kuota penuh, tanpa beralih ke layanan berbayar |
| Potongan terlalu kecil atau terlalu besar | Pencarian mengambil potongan yang kurang tepat | Beberapa ukuran dicoba dengan contoh pertanyaan, hasil dibandingkan dan dicatat (tugas 5) |
| Keputusan *Product Owner* atas penyaringan terlambat | Teks yang dipotong belum final | Pemilihan halaman dibuat dapat diubah lewat pengaturan, sehingga cukup dijalankan ulang setelah keputusan diambil |
| Kalimat terpotong di batas halaman | Informasi terbelah ke dua potongan | Diperiksa pada laporan potongan, dan rujukan halaman tetap dijaga |

## Pernyataan validasi

Berdasarkan kebutuhan informasi PKL di Prodi PTIK, *Sprint Planning* Sprint 2 pada lembar ini, yaitu *Sprint Goal*, *Product Backlog Item* yang dipilih, rencana pengerjaan, serta Increment yang diharapkan, telah divalidasi dan dapat dilaksanakan.

| | |
|---|---|
| Jakarta, 30 Oktober 2026<br>*Product Owner* (Dosen Koordinator PKL),<br><br><br><br>Bambang Satrio, S. Pd., M. Kom.<br>NIP. {{NIP_PRODUCT_OWNER}} | <br>Developer,<br><br><br><br>Deni Merdiansyah<br>NIM {{NIM_DEVELOPER}} |

*Dasar penyusunan: Schwaber & Sutherland (2020) untuk komponen Sprint Planning, Liu et al. (2019) dan Verwijs & Russo (2023) untuk peran perencanaan Sprint yang jelas dan umpan balik pemangku kepentingan. Rujukan lengkap tercantum pada laporan.*
