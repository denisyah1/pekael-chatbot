# Sprint Backlog — Sprint 2

> **Sprint Goal:** Mengubah teks buku panduan PKL yang telah disaring menjadi potongan teks (*chunk*) yang tetap membawa keterangan sumber dan halaman, lalu menjadi representasi vektor menggunakan model embedding Gemini, dengan ukuran potongan awal yang dipilih berdasarkan percobaan, sebagai dasar penyimpanan FAISS dan alur tanya-jawab pada Sprint 3.
> **Periode:** 30 Oktober – 6 November 2026
> **Status task:** `To Do` · `In Progress` · `Done` · `Blocked`
> **Rincian teknis:** [`docs/technical/sprint-02.md`](../../technical/sprint-02.md)

## Task

Sprint Planning memuat enam tugas (lihat [Sprint Planning](sprint_planning.md) bagian 4). Kolom **Tugas** menunjukkan nomor tugas pada Sprint Planning.

| ID | Tugas | PBI | Pekerjaan | Status | Bukti |
|---|---|---|---|---|---|
| S2-T01 | 1 | PBI-01 | Verifikasi akhir koreksi OCR halaman 4–16 oleh Developer (bawaan Sprint 1) | To Do | Lembar pemeriksaan OCR Sprint 1 yang sudah dicentang |
| S2-T02 | 1 | PBI-02 | Keputusan *Product Owner* atas halaman yang dipakai dan bentuk hasil penyaringan (bawaan Sprint 1) | To Do | Keputusan PO pada usulan penyaringan |
| S2-T03 | 2 | PBI-02 | Pemilihan halaman knowledge base lewat pengaturan | Done | Halaman dapat dipilih tanpa mengubah kode, pengujian lulus. Nilai final menunggu S2-T02 |
| S2-T04 | 3 | PBI-03 | Pemotongan teks dengan keterangan sumber, halaman, bagian, dan nomor unik | Done | 26 potongan dari halaman 4–16 dengan label bagian yang tepat, pengujian lulus |
| S2-T05 | 3 | PBI-03 | Skrip laporan potongan untuk beberapa ukuran sekaligus | Done | Laporan empat ukuran potongan (lihat rincian teknis) |
| S2-T06 | 4 | PBI-03 | Integrasi model embedding Gemini untuk dokumen dan pertanyaan, termasuk penyamaan panjang vektor (normalisasi) | To Do | |
| S2-T07 | 4 | PBI-03 | Penanganan batas kuota dan batas panjang masukan embedding | To Do | |
| S2-T08 | 5 | PBI-03 | Percobaan ukuran potongan dan tumpang tindih dengan contoh pertanyaan (EXP-002) | To Do | |
| S2-T09 | 6 | PBI-03 | Statistik potongan dan pemeriksaan konsistensi ukuran vektor | In Progress | Statistik potongan selesai, pemeriksaan vektor menunggu S2-T06 |

## Log Pengerjaan

### 30 Oktober 2026

**Dikerjakan**
- Menyusun *Sprint Planning* Sprint 2 (Lembar Validasi Bagian A).
- Membawa dua pekerjaan Sprint 1 yang belum selesai ke Sprint 2: verifikasi akhir koreksi OCR dan keputusan *Product Owner* atas penyaringan isi.
- Membuat pengaturan pemilihan halaman, sehingga hanya halaman yang disetujui *Product Owner* yang diproses. Nilainya cukup diubah di pengaturan setelah keputusan diambil, tanpa mengubah program.
- Membuat fitur pemotong teks. Setiap potongan menyimpan nama dokumen, halaman PDF, nomor unik, dan bagian buku (judul bab dan subbab). Potongan tidak pernah melewati batas halaman, agar rujukan halaman pada jawaban chatbot tetap tepat.
- Memperbaiki cara penentuan bagian setelah melihat hasil pada teks asli: potongan yang mencakup beberapa subbab kini mencantumkan semua subbab tersebut, dan pergantian BAB dikenali.
- Mencoba empat ukuran potongan pada halaman 4–16 (tanpa memanggil layanan Gemini).

**Hasil uji**
- Pengujian otomatis: 130 lulus, 0 gagal.
- Hasil pemotongan halaman 4–16:

  | Ukuran potongan | Tumpang tindih | Jumlah potongan | Rata-rata panjang (karakter) |
  |---|---|---|---|
  | 500 | 50 | 49 | 340 |
  | 800 | 100 | 33 | 519 |
  | 1.000 | 150 | 26 | 668 |
  | 1.500 | 200 | 18 | 953 |

  Tidak ada potongan kosong atau ganda, dan setiap potongan memiliki label bagian.

**Hambatan**
- Ditemukan satu potongan sangat pendek yang hanya berisi judul ("BAB I Pendahuluan", 36 karakter). Pengaruhnya terhadap pencarian akan dilihat pada percobaan ukuran potongan (S2-T08).
- Keputusan *Product Owner* atas penyaringan masih ditunggu. Untuk sementara dipakai usulan halaman 4–16.

**Berikutnya**
- Integrasi model embedding Gemini (S2-T06, S2-T07).
- Menyiapkan percobaan ukuran potongan dengan contoh pertanyaan dari daftar topik Sprint 1 (S2-T08).
