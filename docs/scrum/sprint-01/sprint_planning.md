# Sprint Planning — Sprint 1

| | |
|---|---|
| Periode | 23 – 29 Oktober 2026 |
| Tanggal planning | 23 Oktober 2026 |
| Peserta | Bambang Satrio, S. Pd., M. Kom. (Product Owner), Dr. Widodo, M. Kom. dan Nur Elah, S. Kom., M.T. (Scrum Master), Deni Merdiansyah (Developer) |
| Fokus (proposal) | Product backlog, persiapan dokumen, OCR, dan penyaringan knowledge base |
| Rincian teknis | [`docs/technical/sprint-01.md`](../../technical/sprint-01.md) |

## Sprint Goal

Isi Buku Pedoman PKL UNJ 2025 berhasil diubah menjadi teks per halaman yang sudah diperiksa kebenarannya dan disetujui Product Owner, sehingga siap dijadikan sumber pengetahuan (knowledge base) chatbot Pekael.

## Kondisi Awal Dokumen

Pemeriksaan awal pada 23 Oktober 2026:

| | |
|---|---|
| Judul | Buku Pedoman Praktik Kerja Lapangan |
| Penerbit | Pusat PKM, PPL, PKL, Magang — Universitas Negeri Jakarta |
| Tahun | 2025 |
| Jumlah halaman | 29 |
| Jenis | **Seluruh halaman hasil scan** (gambar), tidak ada teks digital |
| Kualitas scan | Baik: halaman lurus, teks tajam, latar bersih |

Karena seluruh halaman berupa gambar, **semua halaman harus dibaca dengan OCR**, dan hasilnya wajib dicek manual. Pengecekan ini menjadi pekerjaan terbesar di sprint ini.

## Product Backlog Item yang Diambil

| ID | Item | Prioritas | Kriteria penerimaan |
|---|---|---|---|
| PBI-01 | Ekstraksi teks dari buku panduan PKL hasil scan melalui OCR | Tinggi | Setiap halaman memiliki teks hasil OCR beserta nomor halaman dan sumbernya, angka, tanggal, daftar, dan persyaratan sudah dicek terhadap dokumen asli |
| PBI-02 | Penyaringan dan pengerucutan konten sesuai lingkup PTIK | Tinggi | Bagian buku panduan yang dipakai chatbot sudah ditetapkan dan disetujui Product Owner secara tertulis |

## Sprint Backlog (rencana pekerjaan)

| ID | PBI | Pekerjaan | Estimasi (jam) | Bukti selesai |
|---|---|---|---|---|
| S1-T01 | — | Menyiapkan repository, struktur folder, aturan keamanan API key, dan README awal | — | **Sudah selesai di fase Setup** |
| S1-T02 | — | Mencatat versi library dan menguji FAISS di laptop pengembang | — | **Sudah selesai di fase Setup** |
| S1-T03 | PBI-01 | Mencatat identitas dan versi buku panduan, lalu memvalidasi ruang lingkupnya bersama Product Owner | 1 | Catatan identitas dokumen + persetujuan PO |
| S1-T04 | PBI-01 | Memeriksa apakah tiap halaman berisi teks digital atau hasil scan | 1 | Laporan per halaman (pemeriksaan awal: 29 dari 29 halaman hasil scan) |
| S1-T05 | PBI-01 | Membuat fitur pembaca PDF: teks digital dibaca langsung, halaman scan dibaca dengan OCR Tesseract | 5 | Kode + pengujian otomatis lulus |
| S1-T06 | PBI-01 | Memastikan OCR memakai bahasa Indonesia dan lokasi Tesseract bisa diatur di Windows | 1 | Pengujian OCR lulus |
| S1-T07 | PBI-01 | Merapikan hasil teks (spasi, baris terputus) tanpa mengubah makna, dengan nomor halaman tetap terjaga | 3 | Kode + pengujian otomatis lulus |
| S1-T08 | PBI-01 | Membuat skrip pemeriksa PDF yang menghasilkan laporan ekstraksi dan teks per halaman | 3 | Laporan ekstraksi Buku Pedoman PKL 2025 |
| S1-T09 | PBI-01 | Mengecek hasil OCR ke-29 halaman terhadap dokumen asli, terutama angka, tanggal, tabel, daftar, dan persyaratan | 6 | Lembar pemeriksaan OCR + daftar koreksi |
| S1-T10 | PBI-02 | Menyaring isi buku panduan agar sesuai kebutuhan mahasiswa PTIK, lalu meminta persetujuan Product Owner | 3 | Daftar bagian yang dipakai/dikecualikan + persetujuan PO |
| S1-T11 | PBI-02 | Menyusun daftar topik pertanyaan yang sering ditanyakan mahasiswa, sebagai dasar dataset evaluasi dan UAT | 2 | Daftar topik pertanyaan |
| | | **Total estimasi** | **25** | |

## Definition of Done Sprint Ini

- [ ] Dokumen sumber yang dipakai sudah disetujui Product Owner.
- [ ] Teks setiap halaman tersedia, lengkap dengan nomor halaman dan cara ekstraksinya (OCR atau teks digital).
- [ ] Hasil OCR sudah dicek terhadap dokumen asli, dan koreksinya tercatat.
- [ ] Cara instalasi dan penggunaan OCR terdokumentasi.
- [ ] Pengujian otomatis yang terkait lulus.
- [ ] Tidak ada API key atau dokumen sumber yang ikut ter-upload ke GitHub.
- [ ] Ada bukti validasi sumber dari Product Owner.

## Risiko dan Ketergantungan

| Risiko / ketergantungan | Dampak | Antisipasi |
|---|---|---|
| Seluruh 29 halaman hasil scan, sehingga OCR bisa salah membaca angka atau tanggal | Chatbot memberi informasi keliru | Semua halaman dicek manual, koreksi dicatat dan diterapkan secara konsisten |
| Durasi sprint 1 minggu (Sprint 1–3 dipadatkan karena pengembangan mulai terlambat) | Waktu pengecekan OCR dan validasi PO sempit | Pekerjaan setup sudah selesai lebih dulu, jadwal temu PO diatur sejak awal sprint |
| Ketersediaan waktu Product Owner untuk validasi | Sprint Goal tidak tercapai tepat waktu | Lembar validasi disiapkan lebih awal |

## Keputusan yang Perlu Diambil di Sprint Ini

| ID | Keputusan | Rencana |
|---|---|---|
| OD-16 | Bentuk hasil penyaringan isi buku panduan: (a) PDF baru yang hanya berisi bagian terpilih, atau (b) PDF asli + daftar halaman/bagian yang dikecualikan | Dibahas bersama PO saat S1-T10 |
| OD-17 | Cara menyimpan koreksi hasil OCR agar konsisten setiap kali knowledge base dibangun ulang | Diusulkan: file koreksi per halaman yang diterapkan otomatis saat pembangunan knowledge base, diputuskan saat S1-T09 |
