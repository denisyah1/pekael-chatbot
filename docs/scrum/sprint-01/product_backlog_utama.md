# Product Backlog Utama Pekael

| | |
|---|---|
| Proyek | : Pekael, chatbot layanan informasi PKL berbasis *Retrieval-Augmented Generation* (RAG) untuk mahasiswa Prodi PTIK UNJ |
| Disusun | : 23 Oktober 2026, sebelum *Sprint Planning* Sprint 1 |
| Sumber | : Proposal skripsi (Tabel Product Backlog) dan rencana implementasi proyek |
| *Product Owner* | : Bambang Satrio, S. Pd., M. Kom. (Dosen Koordinator PKL Prodi PTIK UNJ) |
| Developer | : Deni Merdiansyah (NIM {{NIM_DEVELOPER}}) |

## Tujuan

Lembar ini memuat Product Backlog utama Pekael, yaitu delapan item kebutuhan yang harus dihasilkan selama pengembangan. Product Backlog ini menjadi acuan pertama pada setiap *Sprint Planning*: item yang dikerjakan pada suatu sprint dipilih dari daftar ini, dan setiap perubahan item dicatat serta divalidasi *Product Owner*.

## Daftar Product Backlog Item

| ID | Product Backlog Item | Prioritas | Sprint | Kriteria penerimaan | Bukti hasil |
|---|---|---|---|---|---|
| PBI-01 | Ekstraksi teks dari buku panduan PKL hasil scan melalui OCR | Tinggi | 1 | Teks setiap halaman tersedia bersama nomor halaman dan cara pembacaannya, OCR hanya dipakai untuk halaman tanpa teks digital, dan contoh angka, tanggal, serta tabel sudah dicocokkan dengan buku aslinya | Teks terverifikasi dan laporan pembacaan per halaman |
| PBI-02 | Penyaringan dan pengerucutan konten sesuai lingkup PTIK | Tinggi | 1 | Bagian buku yang dipakai sebagai knowledge base telah dipilih dan disetujui *Product Owner* secara tertulis | Daftar halaman terpilih dan bukti validasi *Product Owner* |
| PBI-03 | Pemotongan teks (*text splitting*) dan embedding menjadi representasi vektor | Tinggi | 2 | Setiap potongan teks tetap membawa nama dokumen dan nomor halaman, ukuran vektor seragam, dan percobaan ukuran potongan tercatat | Potongan teks, vektor, dan catatan percobaan |
| PBI-04 | Penyimpanan embedding pada FAISS | Tinggi | 3 | Indeks FAISS dapat dibuat, disimpan, dan dimuat kembali tanpa dibangun ulang | Indeks tersimpan dan hasil uji muat ulang |
| PBI-05 | Alur pencarian dan jawaban (*retrieval chain*) yang menghubungkan FAISS dan Gemini API | Tinggi | 3 | Pertanyaan dijawab hanya dari potongan buku yang ditemukan beserta sumbernya, dan pertanyaan di luar cakupan tidak dijawab dengan tebakan | Alur tanya-jawab dan hasil uji awal |
| PBI-06 | Antarmuka website untuk tanya-jawab | Tinggi | 4 | Mahasiswa dapat mengetik pertanyaan, melihat tanda proses, menerima jawaban, dan melihat pesan yang jelas bila terjadi gangguan | Website Streamlit untuk mahasiswa |
| PBI-07 | Penampilan rujukan sumber pada setiap jawaban | Sedang | 4 | Nama dokumen dan halaman PDF yang tampil hanya berasal dari potongan yang benar-benar dipakai untuk menjawab | Jawaban dengan rujukan yang dapat ditelusuri |
| PBI-08 | Admin mengunggah atau memperbarui dokumen knowledge base | Sedang | 4 | Hanya satu akun admin yang dapat masuk, admin dapat mengunggah dokumen baru, dan knowledge base lama tetap dipakai bila pembaruan gagal | Halaman admin dan proses pembaruan yang aman |

## Rencana sprint

| Sprint | Fokus | Item |
|---|---|---|
| 1 | Persiapan dan validasi knowledge base | PBI-01, PBI-02 |
| 2 | Pemotongan teks dan embedding | PBI-03 |
| 3 | Penyimpanan FAISS dan alur tanya-jawab | PBI-04, PBI-05 |
| 4 | Antarmuka website, rujukan sumber, dan halaman admin | PBI-06, PBI-07, PBI-08 |
| 5 | Validasi ahli dan revisi | Pekerjaan pendukung: dataset evaluasi, pembekuan pengaturan, uji coba Ragas, pemilihan hosting |
| 6 | Penerapan, evaluasi Ragas, UAT, dan analisis | Pekerjaan pendukung: penerapan, evaluasi Ragas, UAT, analisis |

Sprint 5 dan 6 tidak menambah item baru. Kedua sprint tersebut berisi validasi, perbaikan, penerapan kepada pengguna, dan evaluasi terhadap hasil delapan item di atas.

## Definition of Done

Satu item dinyatakan selesai bila syarat berikut yang relevan terpenuhi:

1. Hasilnya sesuai tujuan dan ruang lingkup proposal.
2. Pengaturan yang perlu dicoba-coba tersedia di file pengaturan, dan setiap perubahannya dicatat.
3. Tidak ada API key, kata sandi, dokumen sensitif, atau data responden di repository.
4. Gangguan dasar ditangani dengan pesan yang aman.
5. Pengujian terkait lulus, atau keterbatasan pengujian yang memerlukan layanan berbayar atau API dicatat.
6. Catatan kerja (logbook) diperbarui.
7. Hasilnya dapat diperiksa pada *Sprint Review*.

## Aturan perubahan

1. Status item: Belum dimulai, Dikerjakan, Selesai (menunggu review), Diterima PO, atau Ditunda.
2. Item baru, perubahan kriteria, atau pemindahan item ke sprint lain hanya dilakukan setelah disetujui *Product Owner* dan dicatat beserta tanggal dan alasannya.
3. Status terkini setiap item dan riwayat perubahannya dicatat pada Product Backlog berjalan proyek.

## Pernyataan validasi

Product Backlog utama pada lembar ini telah disusun dari proposal dan disetujui sebagai acuan *Sprint Planning* setiap sprint.

| | |
|---|---|
| Jakarta, 23 Oktober 2026<br>*Product Owner* (Dosen Koordinator PKL),<br><br><br><br>Bambang Satrio, S. Pd., M. Kom.<br>NIP. {{NIP_PRODUCT_OWNER}} | <br>Developer,<br><br><br><br>Deni Merdiansyah<br>NIM {{NIM_DEVELOPER}} |

*Dasar penyusunan: Schwaber & Sutherland (2020) untuk Product Backlog dan Definition of Done. Rujukan lengkap tercantum pada laporan.*
