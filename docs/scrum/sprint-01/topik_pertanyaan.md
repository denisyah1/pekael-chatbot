# Daftar Topik Pertanyaan Mahasiswa — Sprint 1

| | |
|---|---|
| Sumber | : Buku Pedoman PKL UNJ 2025, halaman 4 – 16 (usulan isi knowledge base) |
| Tanggal | : 26 Oktober 2026 |
| Status | : **Draf**, akan divalidasi *Product Owner* |

## Tujuan

Daftar ini memetakan informasi PKL yang kemungkinan besar ditanyakan mahasiswa PTIK, sesuai tugas tambahan Sprint 1 pada spesifikasi proyek. Daftar ini menjadi dasar untuk:

1. dataset evaluasi Ragas (pertanyaan, jawaban acuan, dan konteks acuan disusun pada Sprint 5),
2. pengujian chatbot selama pengembangan (Sprint 3–5),
3. skenario uji coba pengguna (UAT) pada Sprint 6.

Contoh pertanyaan di bawah **belum** merupakan dataset penelitian. Jawaban acuan belum ditulis dan baru disusun serta divalidasi pada Sprint 5.

## Topik pertanyaan yang tercakup buku panduan

| No | Topik | Hal. | Contoh pertanyaan | Jenis pertanyaan |
|---|---|---|---|---|
| 1 | Pengertian PKL | 5 | Apa yang dimaksud dengan Praktik Kerja Lapangan? | Langsung |
| 2 | Dasar hukum PKL | 4–5 | PKL di UNJ mengacu pada peraturan apa saja? | Daftar |
| 3 | Tujuan PKL | 5–6 | Apa tujuan dilaksanakannya PKL? | Daftar |
| 4 | Manfaat PKL | 6–7 | PKL bermanfaat apa untuk mahasiswa? Untuk mitra? | Daftar, beberapa bagian |
| 5 | Lama pelaksanaan | 7, 14 | Berapa lama PKL harus dilaksanakan? | Angka |
| 6 | Jenis tempat PKL | 7 | Di mana saja PKL boleh dilaksanakan? | Daftar |
| 7 | Mengusulkan tempat sendiri | 7 | Bolehkah saya mencari tempat PKL sendiri? Apa syaratnya? | Persyaratan, parafrasa |
| 8 | Tugas koordinator prodi dan koordinator PKL | 7–8 | Siapa yang menetapkan tempat dan dosen pembimbing PKL? | Langsung |
| 9 | Tugas dosen pembimbing | 8–9 | Apa saja tugas dosen pembimbing PKL? | Daftar |
| 10 | Tugas pembimbing lapangan (mentor) | 9 | Apa peran mentor di tempat PKL? | Daftar |
| 11 | Kewajiban mahasiswa peserta PKL | 9–10 | Apa saja kewajiban saya selama PKL? | Daftar |
| 12 | Syarat minimal SKS | 10 | Berapa SKS minimal untuk bisa ikut PKL? | Angka, persyaratan |
| 13 | Mata kuliah prasyarat | 10 | Mata kuliah apa saja yang harus sudah ditempuh sebelum PKL? | Persyaratan |
| 14 | PKL internasional | 11 | Apa syarat tambahan kalau PKL di luar negeri? | Persyaratan |
| 15 | Syarat kelulusan PKL | 11 | Kapan saya dinyatakan lulus PKL? | Persyaratan, daftar |
| 16 | Kondisi harus mengulang | 11 | Dalam kondisi apa mahasiswa harus mengulang PKL? | Daftar |
| 17 | Tata tertib | 11 | Apa aturan berpakaian dan kehadiran selama PKL? | Daftar |
| 18 | Izin tidak hadir | 10–11 | Bagaimana kalau saya sakit saat PKL? | Prosedur, beberapa bagian |
| 19 | Alur pengajuan PKL | 13 | Bagaimana langkah-langkah mengajukan PKL? | Prosedur bertahap |
| 20 | Pendaftaran di SIAKAD | 13 | Di mana saya mendaftar PKL? | Langsung |
| 21 | Bobot dan jumlah SKS PKL | 13–14 | PKL berapa SKS dan berapa menit per minggu? | Angka |
| 22 | Alur pelaksanaan PKL | 14 | Apa saja tahapan setelah saya diterima di tempat PKL? | Prosedur bertahap |
| 23 | Pembekalan PKL | 8, 14 | Apakah ada pembekalan sebelum PKL? Siapa yang menyelenggarakan? | Langsung, beberapa bagian |
| 24 | Laporan dan presentasi | 9, 10, 14 | Kepada siapa laporan PKL diserahkan? | Daftar |
| 25 | Sanksi mahasiswa | 14–15 | Apa sanksinya jika saya tidak menyelesaikan PKL tepat waktu? | Persyaratan |
| 26 | Sanksi dosen pembimbing | 15 | Apa yang terjadi kalau dosen pembimbing tidak membimbing? | Langsung |
| 27 | Aspek penilaian | 16 | Apa saja aspek yang dinilai dalam PKL? | Daftar |
| 28 | Konversi nilai | 16 | Nilai B+ itu berapa rentang angkanya? | Angka |
| 29 | Hubungan nilai dan kelulusan | 11, 16 | Kalau nilai saya 74, apakah saya lulus PKL? | Angka, beberapa bagian |
| 30 | Parafrasa santai | 7 | PKL-nya berapa bulan sih kak? | Parafrasa |

## Pertanyaan tentang PKL yang **tidak** dijawab buku panduan

Pertanyaan ini wajar ditanyakan mahasiswa, tetapi jawabannya tidak ada di buku panduan. Chatbot harus menyatakan informasi tidak tersedia (fallback), bukan menebak.

| No | Contoh pertanyaan | Alasan di luar cakupan |
|---|---|---|
| L1 | Kapan batas akhir pendaftaran PKL semester ini? | Tanggal pendaftaran tidak tercantum |
| L2 | Kapan jadwal pembekalan PKL tahun ini? | Jadwal tidak tercantum |
| L3 | Perusahaan mana yang sedang membuka lowongan PKL untuk mahasiswa PTIK? | Informasi lowongan di luar ruang lingkup penelitian |
| L4 | Siapa koordinator PKL Prodi PTIK saat ini? | Nama pejabat tidak tercantum |
| L5 | Bagaimana format margin dan huruf laporan PKL? | Panduan penulisan laporan dikecualikan dari knowledge base |

## Pertanyaan di luar topik PKL

| No | Contoh pertanyaan |
|---|---|
| N1 | Bagaimana cara mengajukan beasiswa di UNJ? |
| N2 | Apa itu machine learning? |
| N3 | Buatkan saya puisi tentang kampus. |

Pertanyaan pada dua tabel terakhir dipakai untuk mengkalibrasi batas relevansi (Sprint 3–5) dan diuji terpisah dari dataset Ragas utama, sesuai rancangan evaluasi.
