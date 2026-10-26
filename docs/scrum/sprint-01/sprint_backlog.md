# Sprint Backlog — Sprint 1

> **Sprint Goal:** Isi Buku Pedoman PKL UNJ 2025 berhasil diubah menjadi teks per halaman yang sudah diperiksa kebenarannya dan disetujui Product Owner, sehingga siap dijadikan sumber pengetahuan (knowledge base) chatbot Pekael.
> **Periode:** 23 – 29 Oktober 2026
> **Status task:** `To Do` · `In Progress` · `Done` · `Blocked`
> **Rincian teknis:** [`docs/technical/sprint-01.md`](../../technical/sprint-01.md)

## Task

| ID | PBI | Pekerjaan | Status | Bukti |
|---|---|---|---|---|
| S1-T01 | — | Repository, struktur folder, aturan keamanan API key, README awal | Done | Fase Setup ([`setup_phase.md`](../setup_phase.md)) |
| S1-T02 | — | Pencatatan versi library dan uji FAISS | Done | Fase Setup ([`setup_phase.md`](../setup_phase.md)) |
| S1-T03 | PBI-01 | Identitas dokumen dan validasi lingkup bersama PO | In Progress | Identitas dokumen sudah dicatat, sumber disetujui saat validasi planning |
| S1-T04 | PBI-01 | Pemeriksaan teks digital vs hasil scan per halaman | Done | Laporan ekstraksi: 29 dari 29 halaman hasil scan, semua dibaca dengan OCR |
| S1-T05 | PBI-01 | Fitur pembaca PDF + OCR | Done | Pembaca PDF berjalan pada ke-29 halaman, pengujian otomatis lulus |
| S1-T06 | PBI-01 | OCR bahasa Indonesia + pengaturan lokasi Tesseract | Done | OCR memakai bahasa Indonesia dan Inggris, lokasi Tesseract diatur lewat konfigurasi, pengujian lulus |
| S1-T07 | PBI-01 | Perapian teks tanpa mengubah makna | Done | Perapian spasi, baris terputus, dan judul, pengujian lulus |
| S1-T08 | PBI-01 | Skrip pemeriksa PDF + laporan ekstraksi | Done | Laporan ekstraksi Buku Pedoman PKL 2025 (lihat rincian teknis) |
| S1-T09 | PBI-01 | Pengecekan hasil OCR 29 halaman | In Progress | Halaman prioritas sudah ditentukan, hal. 19 dan 28 sudah dicek |
| S1-T10 | PBI-02 | Penyaringan isi + persetujuan PO | In Progress | [Usulan penyaringan](usulan_penyaringan.md) siap dibahas dengan PO |
| S1-T11 | PBI-02 | Daftar topik pertanyaan mahasiswa | To Do | |

## Log Pengerjaan

### 23 Oktober 2026

**Dikerjakan**
- Menyusun Sprint Planning dan Lembar Validasi Planning Sprint 1.
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
