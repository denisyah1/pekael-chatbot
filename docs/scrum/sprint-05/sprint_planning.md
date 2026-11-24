# Lembar Validasi Sprint Report 5 — Bagian A: Sprint Planning

| | |
|---|---|
| Sprint | : Sprint 5 |
| Periode Sprint | : 20 – 26 November 2026 |
| *Product Owner* (validator) | : Dosen Koordinator PKL Prodi PTIK UNJ |
| Scrum Master | : Dosen pembimbing |
| Developer | : Deni Merdiansyah (NIM {{NIM_DEVELOPER}}) |

## Tujuan

Lembar ini memuat hasil *Sprint Planning* Sprint 5 untuk divalidasi oleh *Product Owner* dari sisi kebenaran isi jawaban, dataset evaluasi, dan urutan pengerjaan, sebelum Sprint 5 dikerjakan. Sesuai Scrum Guide, *Sprint backlog* terdiri atas *Sprint Goal*, item yang dipilih untuk Sprint, dan rencana pengerjaannya, ketiganya disajikan pada bagian 2 sampai 4.

## *Sprint Goal*

Menghasilkan kandidat Pekael yang isinya sudah divalidasi *Product Owner*: knowledge base mencakup Buku Pedoman PKL dan dokumen knowledge base tambahan dari *Product Owner*, dataset evaluasi sekitar 30 pertanyaan beserta jawaban acuan telah divalidasi, pengaturan pencarian dan instruksi jawaban dibekukan untuk evaluasi akhir, dan uji coba evaluasi Ragas dengan layanan gratis berjalan, sehingga Sprint 6 dapat langsung dipakai untuk penerapan, evaluasi, dan UAT.

## Item yang dipilih

| No | Item | Prioritas | Alasan dipilih pada Sprint 5 |
|---|---|---|---|
| 1 | Dataset ground truth dan validasi oleh *Product Owner* (SUP-01) | Tinggi | Evaluasi Ragas pada Sprint 6 memerlukan pertanyaan dan jawaban acuan yang sudah benar menurut *Product Owner* |
| 2 | Kalibrasi dan pembekuan pengaturan (SUP-02) | Tinggi | Hasil evaluasi akhir hanya sah bila pengaturan tidak berubah selama pengumpulan data |
| 3 | Uji coba evaluasi Ragas (SUP-03) | Tinggi | Evaluator harus terbukti berjalan sebelum dataset akhir dinilai |
| 4 | Pemilihan hosting dan estimasi biaya (SUP-04) | Sedang | UAT minimal 100 responden pada Sprint 6 memerlukan website yang dapat diakses publik |
| 5 | Penambahan dokumen knowledge base dari *Product Owner* (lanjutan PBI-02 dan PBI-08) | Tinggi | *Product Owner* menyerahkan dokumen tambahan berisi contoh pertanyaan, jawaban lengkap, dan penjelasan |

## Rencana pengerjaan (*Sprint backlog*)

| | |
|---|---|
| Masukan | : Website hasil Sprint 4, Buku Pedoman PKL 2025 halaman 4–16, 22–25, 27–28, dokumen knowledge base tambahan dari *Product Owner* (8 halaman), 36 pertanyaan uji Sprint 4 |
| Alat | : LangChain, FAISS, model Gemini `gemini-3.5-flash-lite`, Ragas dengan evaluator Groq versi gratis |
| Prinsip | : Isi jawaban hanya dari dokumen yang disetujui *Product Owner*, setiap perubahan pengaturan dicatat, evaluasi memakai layanan tanpa biaya |

| No | Tugas | Item terkait | Keluaran | Waktu |
|---|---|---|---|---|
| 1 | Memeriksa ulang label halaman daftar topik pertanyaan (dibawa dari Sprint 4) | 1 | Daftar topik yang diperbarui | 20 – 21 November 2026 |
| 2 | Memasukkan dokumen knowledge base tambahan dari *Product Owner* ke knowledge base, dengan rujukan nama dokumen dan halaman | 5 | Knowledge base dua dokumen | 20 November 2026 |
| 3 | Mengganti evaluator Ragas dari OpenAI (berbayar) ke Groq versi gratis dan menguji ketiga metrik dengan satu contoh | 3 | Hasil uji evaluator | 20 – 21 November 2026 |
| 4 | Menyusun dataset ground truth awal sekitar 30 pertanyaan beserta jawaban acuan dan konteks rujukan dari knowledge base | 1 | Dataset evaluasi awal | 21 – 22 November 2026 |
| 5 | Validasi kebenaran sumber, jawaban acuan, dan keterwakilan pertanyaan bersama *Product Owner* | 1 | Dataset tervalidasi | 23 November 2026 |
| 6 | Menguji pertanyaan angka, tanggal, persyaratan, parafrasa, multi-bagian, pertanyaan yang tidak tercakup, dan non-PKL, serta mengukur waktu jawab pada pagi, siang, dan malam | 2 | Hasil uji kasus dan waktu jawab | 21 – 24 November 2026 |
| 7 | Kalibrasi lalu membekukan jumlah potongan, batas kedekatan, ukuran potongan, dan instruksi jawaban | 2 | Konfigurasi evaluasi akhir tercatat | 24 November 2026 |
| 8 | Uji coba Ragas pada beberapa entri dataset | 3 | Hasil uji coba Ragas | 24 – 25 November 2026 |
| 9 | Pengelolaan dokumen tambahan di ruang admin (melihat, menambah, dan melepas dokumen tambahan) | 5 | Ruang admin untuk beberapa dokumen | 21 – 25 November 2026 |
| 10 | Memeriksa enam pernyataan UAT pada Tabel 3.7 terhadap jumlah item per kategori, meminta keputusan pembimbing bila perlu | 4 | Instrumen UAT yang diperiksa | 25 November 2026 |
| 11 | Membandingkan pilihan hosting dan menetapkan platform beserta estimasi biaya | 4 | Keputusan hosting | 25 – 26 November 2026 |

## Increment dan kriteria selesai

| Increment | Kriteria selesai | Titik validasi |
|---|---|---|
| Knowledge base dua dokumen | Jawaban dapat bersumber dari Buku Pedoman dan dokumen tambahan, rujukan menyebut nama dokumen dan halaman PDF, versi lama tetap dapat diaktifkan kembali | *Product Owner* mencoba pertanyaan pada *Sprint Review* |
| Dataset evaluasi | Sekitar 30 pertanyaan dengan jawaban acuan dan konteks rujukan, divalidasi *Product Owner* | Tanda tangan *Product Owner* pada lembar validasi dataset |
| Konfigurasi evaluasi akhir | Pengaturan pencarian dan instruksi jawaban dibekukan dan dicatat, uji coba Ragas ketiga metrik berjalan | Peneliti memeriksa, dikonfirmasi pada *Sprint Review* |
| Keputusan hosting | Platform dan estimasi biaya disetujui sebelum UAT publik | Developer dan dosen pembimbing |

## Peran dan keterlibatan pada Sprint 5

| Peran | Pemegang | Keterlibatan | Keluaran |
|---|---|---|---|
| *Product Owner* | Dosen koordinator PKL | Menyerahkan dokumen knowledge base tambahan, memvalidasi dataset evaluasi dan isi jawaban, mencoba website pada *Sprint Review* | Bukti validasi |
| Scrum Master | Dosen pembimbing | Memastikan *Sprint Planning*, *Sprint Review*, dan *Sprint Retrospective* terlaksana, memberi keputusan instrumen UAT bila diperlukan | Konfirmasi checklist |
| Developers | Peneliti | Mengerjakan *Sprint backlog* dan mengisi logbook setiap hari kerja aktif | Logbook, Increment |

## Jadwal peristiwa Sprint 5

| Peristiwa | Waktu | Pelaksana |
|---|---|---|
| *Sprint Planning* | 20 November 2026 | Peneliti, *Product Owner* |
| Pengerjaan harian (logbook) | 20 – 26 November 2026 | Peneliti |
| Validasi dataset evaluasi | 23 November 2026 | Peneliti, *Product Owner* |
| *Sprint Review* | 26 November 2026 | Peneliti, *Product Owner*, Scrum Master |
| *Sprint Retrospective* | 26 November 2026 | Peneliti, Scrum Master |

## Risiko dan penanganan

| Risiko | Dampak | Penanganan |
|---|---|---|
| Isi dokumen tambahan berbeda dengan Buku Pedoman | Jawaban membingungkan mahasiswa | Dokumen tambahan menyebut perbedaannya dan ketentuan Prodi PTIK didahulukan, perbedaan diperiksa bersama *Product Owner* |
| Batas layanan gratis Groq atau Gemini tercapai saat evaluasi | Evaluasi terhenti di tengah | Uji coba dengan sedikit entri lebih dulu, jeda antar permintaan, jumlah permintaan dicatat |
| Penambahan dokumen mengubah jarak kedekatan pertanyaan | Batas kedekatan 0,64 tidak lagi memisahkan pertanyaan PKL dan non-PKL | Uji ulang seluruh pertanyaan uji setiap kali knowledge base berubah, sebelum pengaturan dibekukan |
| Validasi dataset oleh *Product Owner* tertunda | Evaluasi Sprint 6 mundur | Dataset awal diserahkan paling lambat 22 November 2026 |

## Pernyataan validasi

Berdasarkan kebutuhan informasi PKL di Prodi PTIK, *Sprint Planning* Sprint 5 pada lembar ini, yaitu *Sprint Goal*, item yang dipilih, rencana pengerjaan, serta Increment yang diharapkan, telah divalidasi dan dapat dilaksanakan.

| | |
|---|---|
| Jakarta, 20 November 2026<br>*Product Owner* (Dosen Koordinator PKL),<br><br><br><br>Bambang Satrio, S. Pd., M. Kom.<br>NIP. {{NIP_PRODUCT_OWNER}} | <br>Developer,<br><br><br><br>Deni Merdiansyah<br>NIM {{NIM_DEVELOPER}} |

*Dasar penyusunan: Schwaber & Sutherland (2020) untuk komponen Sprint Planning, Liu et al. (2019) dan Verwijs & Russo (2023) untuk peran perencanaan Sprint yang jelas dan umpan balik pemangku kepentingan. Rujukan lengkap tercantum pada laporan.*
