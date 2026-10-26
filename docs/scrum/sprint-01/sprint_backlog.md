# Sprint Backlog — Sprint 1

> **Sprint Goal:** Menyiapkan teks buku panduan PKL yang telah diekstraksi dan diverifikasi, serta knowledge base yang telah disaring sesuai lingkup Prodi PTIK, sebagai dasar tahap text splitting dan embedding pada Sprint 2.
> **Periode:** 23 – 29 Oktober 2026
> **Status task:** `To Do` · `In Progress` · `Done` · `Blocked`
> **Rincian teknis:** [`docs/technical/sprint-01.md`](../../technical/sprint-01.md)

## Task

Sprint Planning memuat lima tugas (lihat [Sprint Planning](sprint_planning.md) bagian 4). Tabel ini merinci tugas tersebut menjadi pekerjaan yang lebih kecil. Kolom **Tugas** menunjukkan nomor tugas pada Sprint Planning.

| ID | Tugas | PBI | Pekerjaan | Status | Bukti |
|---|---|---|---|---|---|
| S1-T01 | Setup | — | Repository, struktur folder, aturan keamanan API key, README awal | Done | Fase Setup ([`setup_phase.md`](../setup_phase.md)) |
| S1-T02 | Setup | — | Pencatatan versi library dan uji FAISS | Done | Fase Setup ([`setup_phase.md`](../setup_phase.md)) |
| S1-T03 | 1 | PBI-01 | Identitas dokumen dan validasi lingkup bersama PO | In Progress | Identitas dokumen sudah dicatat, sumber disetujui saat validasi planning |
| S1-T04 | 1 | PBI-01 | Pemeriksaan teks digital vs hasil scan per halaman | Done | Laporan ekstraksi: 29 dari 29 halaman hasil scan, semua dibaca dengan OCR |
| S1-T05 | 2 | PBI-01 | Fitur pembaca PDF + OCR | Done | Pembaca PDF berjalan pada ke-29 halaman, pengujian otomatis lulus |
| S1-T06 | 2 | PBI-01 | OCR bahasa Indonesia + pengaturan lokasi Tesseract | Done | OCR memakai bahasa Indonesia dan Inggris, lokasi Tesseract diatur lewat konfigurasi, pengujian lulus |
| S1-T07 | 3 | PBI-01 | Perapian teks tanpa mengubah makna | Done | Perapian spasi, baris terputus, dan judul, pengujian lulus |
| S1-T08 | 2 | PBI-01 | Skrip pemeriksa PDF + laporan ekstraksi | Done | Laporan ekstraksi Buku Pedoman PKL 2025 (lihat rincian teknis) |
| S1-T09 | 3 | PBI-01 | Pengecekan hasil OCR 29 halaman | In Progress | [Lembar pemeriksaan OCR](pemeriksaan_ocr.md): hal. 4–16 sudah diperiksa dan dikoreksi, menunggu verifikasi Developer |
| S1-T10 | 4, 5 | PBI-02 | Penyaringan isi + persetujuan PO | In Progress | [Usulan penyaringan](usulan_penyaringan.md) siap dibahas dengan PO |
| S1-T11 | Tambahan (spec §12) | PBI-02 | Daftar topik pertanyaan mahasiswa | To Do | |
| S1-T12 | Tambahan | — | Membuat skrip ekspor dokumen Scrum ke Word dan PDF sesuai template laporan (ditambahkan selama sprint atas permintaan Developer) | Done | Dokumen Sprint 1, Product Backlog, dan laporan fase Setup berhasil diekspor ke Word dan PDF |

Keterangan: **Setup** = pekerjaan yang sudah tuntas pada fase Setup. **Tambahan** = pekerjaan di luar lima tugas planning: daftar topik pertanyaan diwajibkan oleh spesifikasi proyek untuk Sprint 1, dan skrip ekspor dokumen ditambahkan selama sprint.

## Log Pengerjaan

### 23 Oktober 2026

**Dikerjakan**
- Melaksanakan Sprint Planning Sprint 1 bersama Product Owner dan menyusun Lembar Validasi Sprint Report 1 Bagian A.
- Memeriksa awal Buku Pedoman PKL 2025: 29 halaman, seluruhnya hasil scan dengan kualitas baik. Artinya semua halaman akan dibaca dengan OCR.
- Mencatat identitas dokumen (judul, penerbit, tahun, jumlah halaman, sidik file) agar versi dokumen yang dipakai bisa ditelusuri.

**Hasil uji**
- Belum ada pengujian baru, sprint menunggu validasi planning oleh PO.

**Hambatan**
- Durasi sprint hanya 1 minggu karena pengembangan dimulai lebih lambat dari rencana awal.

**Berikutnya**
- Product Owner menandatangani Lembar Validasi Planning.
- Mulai membuat fitur pembaca PDF dan OCR (S1-T05, S1-T06).

### 26 Oktober 2026

**Dikerjakan**
- Membuat fitur pembaca PDF. Halaman yang memiliki teks digital dibaca langsung, sedangkan halaman hasil scan dibaca dengan OCR. Setiap halaman menyimpan nama dokumen, nomor halaman, cara pembacaannya, dan sidik file.
- Membuat fitur perapian teks yang hanya membereskan spasi, baris yang terputus, dan judul, tanpa mengubah kata, angka, atau tanda baca.
- Membuat skrip pemeriksa PDF yang menghasilkan teks per halaman dan laporan ekstraksi, termasuk tingkat keyakinan OCR per halaman untuk menentukan halaman yang perlu dicek lebih teliti.
- Membandingkan pembacaan OCR pada dua resolusi (200 dan 300 dpi). Resolusi 200 dpi, yang sama dengan resolusi scan aslinya, memberi hasil yang lebih tepat dan lebih cepat, sehingga dipilih (EXP-001).
- Membaca ke-29 halaman Buku Pedoman dengan OCR. Rata-rata tingkat keyakinan sekitar 90%.
- Mengecek dua halaman dengan keyakinan terendah:
  - Halaman 19: teks paragraf terbaca baik, tetapi contoh garis titik-titik terbaca sebagai huruf acak, dan "BAB II" terbaca "BAB IL".
  - Halaman 28: berupa tabel penilaian. OCR tidak dapat membaca susunan tabel dengan benar, sehingga halaman ini perlu ditulis ulang manual.
- Menyusun peta isi buku dan [usulan penyaringan](usulan_penyaringan.md): bagian prosedur, persyaratan, dan tahapan (hal. 4–16) diusulkan dipakai, sedangkan panduan penulisan laporan (hal. 17–26) diusulkan dikecualikan sesuai batasan penelitian.

**Hasil uji**
- Pengujian otomatis: 90 lulus, 0 gagal.
- Ekstraksi Buku Pedoman: 29 dari 29 halaman berhasil dibaca dengan OCR dalam waktu sekitar 2 menit.

**Hambatan**
- Halaman berbentuk tabel dan formulir tidak dapat dibaca OCR dengan rapi. Solusi yang diusulkan: hasilnya ditulis ulang manual dan disimpan sebagai koreksi (OD-17).

**Berikutnya**
- Melanjutkan pengecekan OCR untuk halaman lain, terutama halaman yang diusulkan masuk knowledge base.
- Membahas usulan penyaringan bersama Product Owner.
- Menyusun daftar topik pertanyaan mahasiswa (S1-T11).

### 26 Oktober 2026 (lanjutan)

**Dikerjakan**
- Menambahkan pekerjaan baru ke Sprint Backlog (S1-T12): dokumen Scrum perlu bisa diubah ke Word dan PDF untuk laporan dan lembar validasi.
- Membuat skrip ekspor yang mengubah semua dokumen Scrum menjadi Word dan PDF dengan tampilan yang sama seperti template Lembar Validasi Sprint Report: logo UNJ, judul penelitian, huruf Times New Roman, dan ukuran A4. Setiap dokumen hanya berbeda pada judul di bagian header dan keterangan di bagian bawah halaman.
- Menjaga data pribadi: NIP dan NIM tidak disimpan di repository publik, tetapi diisi otomatis dari pengaturan lokal saat dokumen diekspor. File template asli yang memuat NIP dan NIM juga tidak ikut diunggah.

**Hasil uji**
- Pengujian otomatis: 100 lulus, 0 gagal.
- Enam dokumen (Sprint Planning, Lembar Validasi Planning, Sprint Backlog, Usulan Penyaringan, Product Backlog, Laporan Fase Setup) berhasil diekspor ke Word dan PDF, lalu tampilannya diperiksa.

**Berikutnya**
- Melanjutkan pengecekan OCR (S1-T09) dan penyusunan daftar topik pertanyaan (S1-T11).

### 26 Oktober 2026 (sesi 3)

**Dikerjakan**
- Menyamakan dokumen Sprint Planning dengan Lembar Validasi Sprint Report 1 yang telah disusun dan divalidasi. Sprint Planning dan lembar validasinya kini menjadi satu dokumen (Bagian A). Templat untuk sprint berikutnya disusun dengan format yang sama: Bagian A Sprint Planning, Bagian B Sprint Review, Bagian C Sprint Retrospective.
- Memetakan pekerjaan rinci pada Sprint Backlog ke lima tugas Sprint Planning.
- Memeriksa hasil OCR halaman 4–16 dengan membandingkan gambar halaman dan teks hasil OCR kata demi kata ([lembar pemeriksaan](pemeriksaan_ocr.md)):
  - 4 halaman benar seluruhnya, 6 halaman hanya perlu koreksi kecil (huruf, tanda baca, spasi).
  - Semua angka dan ketentuan penting terbaca benar: masa PKL minimal 4 bulan, minimal 100 SKS, nilai kelulusan minimal B+, 170 menit per SKS, dan 6 SKS.
  - Dua bagan prosedur (hal. 13 dan 14) dan tabel konversi nilai (hal. 16) tidak terbaca oleh OCR, sehingga ditulis ulang secara manual sesuai gambar asli.
- Membuat fitur koreksi: teks yang sudah diperbaiki disimpan per halaman dan dipakai otomatis setiap kali knowledge base dibangun. Koreksi terikat pada versi dokumen, sehingga tidak ikut terpakai bila PDF diganti.

**Hasil uji**
- Pengujian otomatis: 105 lulus, 0 gagal.
- Ekstraksi ulang halaman 4–16: koreksi terpasang pada 9 halaman (4, 5, 6, 8, 10, 11, 13, 14, 16).

**Hambatan**
- Bagan dan tabel tidak dapat dibaca OCR. Diatasi dengan penulisan ulang manual yang perlu diverifikasi Developer.

**Berikutnya**
- Developer memverifikasi lembar pemeriksaan OCR terhadap dokumen asli.
- Membahas usulan penyaringan dan lampiran penilaian (hal. 27–28) bersama Product Owner.
- Menyusun daftar topik pertanyaan mahasiswa (S1-T11).
