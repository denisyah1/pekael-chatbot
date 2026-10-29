# Sprint Backlog — Sprint 2

> **Sprint Goal:** Mengubah teks buku panduan PKL yang telah disaring menjadi potongan teks (*chunk*) yang tetap membawa keterangan sumber dan halaman, lalu menjadi representasi vektor menggunakan model embedding Gemini, dengan ukuran potongan awal yang dipilih berdasarkan percobaan, sebagai dasar penyimpanan FAISS dan alur tanya-jawab pada Sprint 3.
> **Periode:** 30 Oktober – 5 November 2026
> **Status task:** `To Do` · `In Progress` · `Done` · `Blocked`
> **Rincian teknis:** [`docs/technical/sprint-02.md`](../../technical/sprint-02.md)

## Task

Sprint Planning memuat enam tugas (lihat [Sprint Planning](sprint_planning.md) bagian 4). Kolom **Tugas** menunjukkan nomor tugas pada Sprint Planning.

| ID | Tugas | PBI | Pekerjaan | Status | Bukti |
|---|---|---|---|---|---|
| S2-T01 | 1 | PBI-01 | Verifikasi akhir koreksi OCR halaman 4–16 oleh Developer (bawaan Sprint 1) | Done | Developer membandingkan koreksi dengan buku asli dan menyatakannya akurat, tanpa perubahan |
| S2-T02 | 1 | PBI-02 | Keputusan *Product Owner* atas halaman yang dipakai dan bentuk hasil penyaringan (bawaan Sprint 1) | To Do | Keputusan PO pada usulan penyaringan |
| S2-T03 | 2 | PBI-02 | Pemilihan halaman knowledge base lewat pengaturan | Done | Halaman dapat dipilih tanpa mengubah kode, pengujian lulus. Nilai final menunggu S2-T02 |
| S2-T04 | 3 | PBI-03 | Pemotongan teks dengan keterangan sumber, halaman, bagian, dan nomor unik | Done | 26 potongan dari halaman 4–16 dengan label bagian yang tepat, pengujian lulus |
| S2-T05 | 3 | PBI-03 | Skrip laporan potongan untuk beberapa ukuran sekaligus | Done | Laporan empat ukuran potongan (lihat rincian teknis) |
| S2-T06 | 4 | PBI-03 | Integrasi model embedding Gemini untuk dokumen dan pertanyaan, termasuk penyamaan panjang vektor (normalisasi) | Done | Vektor 768 angka untuk potongan dan pertanyaan, diuji langsung ke layanan Gemini dan dengan pengujian otomatis |
| S2-T07 | 4 | PBI-03 | Penanganan batas kuota dan batas panjang masukan embedding | Done | Coba ulang otomatis terbukti saat percobaan, teks terlalu panjang ditolak dengan pesan jelas |
| S2-T08 | 5 | PBI-03 | Percobaan ukuran potongan dan tumpang tindih dengan contoh pertanyaan (EXP-002) | Done | Catatan percobaan EXP-002, parameter awal 1.000/150 dipertahankan |
| S2-T09 | 6 | PBI-03 | Statistik potongan dan pemeriksaan konsistensi ukuran vektor | Done | Statistik empat ukuran potongan, semua vektor berukuran 768 |

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

### 30 Oktober 2026 (lanjutan)

**Dikerjakan**
- Developer memverifikasi koreksi OCR halaman 4–16 terhadap buku asli dan menyatakannya akurat (S2-T01 selesai).
- Developer mengusulkan halaman 22–25 (sistematika laporan PKL) ikut dipakai. Karena halaman tersebut berada di luar ruang lingkup proposal, usulan dicatat sebagai perubahan ruang lingkup yang menunggu keputusan *Product Owner*. Sampai ada keputusan, knowledge base memakai halaman 4–16.
- Periode Sprint 2 ditetapkan 30 Oktober – 5 November 2026, Sprint 3 tetap 6 – 12 November 2026.
- Membuat penghubung ke model embedding Gemini. Potongan teks dan pertanyaan masing-masing diubah menjadi 768 angka (vektor) dengan cara yang sesuai untuk pencarian, lalu panjang vektornya disamakan.
- Menambahkan pengaman: bila kuota layanan penuh, sistem menunggu lalu mencoba lagi paling banyak tiga kali tanpa beralih ke layanan berbayar. Teks yang terlalu panjang ditolak, karena uji langsung menunjukkan layanan diam-diam memotong teks panjang.
- Menjalankan percobaan ukuran potongan (EXP-002) dengan 30 contoh pertanyaan dan 8 pertanyaan di luar cakupan, serta membandingkan ukuran vektor 768 dan 3072.

**Hasil uji**
- Pengujian otomatis: 143 lulus, 0 gagal.
- Uji langsung ke Gemini: vektor 768 angka dengan panjang 1,0 setelah disamakan.
- Hasil percobaan: untuk keempat ukuran potongan, 29 dari 30 pertanyaan menemukan halaman yang tepat di empat hasil teratas, dan 25–26 pertanyaan di urutan pertama. Perbedaannya hanya satu pertanyaan, sehingga ukuran awal 1.000 karakter dengan tumpang tindih 150 dipertahankan. Ukuran vektor 3072 juga hanya unggul satu pertanyaan, sehingga 768 dipakai. Pertanyaan yang "meleset" ternyata mengambil halaman 13 yang juga relevan, label halamannya yang kurang lengkap dan sudah diperbaiki.
- Saat percobaan, layanan Gemini dua kali menolak sementara karena sibuk atau kuota. Sistem menunggu lalu berhasil melanjutkan, sesuai rancangan.

**Hambatan**
- Pertanyaan PKL yang jawabannya tidak ada di buku (misalnya jadwal pendaftaran) memiliki kemiripan yang hampir sama dengan pertanyaan yang bisa dijawab. Ini tidak bisa diatasi dengan pencarian saja, dan akan ditangani lewat instruksi kepada Gemini pada Sprint 3.

**Berikutnya**
- Keputusan *Product Owner* atas penyaringan halaman, termasuk usulan halaman 22–25 (S2-T02).
- Menyiapkan *Sprint Review* dan *Sprint Retrospective* Sprint 2 (5 November 2026).

### 31 Oktober 2026

**Dikerjakan**
- Menyusun draf Lembar Validasi Bagian B ([Sprint Review](sprint_review.md)) dan Bagian C ([Sprint Retrospective](sprint_retrospective.md)) untuk pertemuan 5 November 2026. Status pencapaian *Sprint Goal*, masukan *Product Owner*, keputusan validasi, dan tanda tangan diisi saat pertemuan.
- Memeriksa tindak lanjut rencana perbaikan Sprint 1: penulisan tanggal, templat dokumen, dan pemeriksa API key sudah terlaksana. Penjadwalan validasi *Product Owner* di pertengahan sprint belum terlaksana.

**Hasil uji**
- Tidak ada perubahan program. Dokumen Sprint 2 diekspor ulang ke Word dan PDF.

**Berikutnya**
- Pertemuan dengan *Product Owner* pada 5 November 2026: *Sprint Review* Sprint 1 dan Sprint 2, keputusan penyaringan halaman (S2-T02), termasuk usulan halaman 22–25.
