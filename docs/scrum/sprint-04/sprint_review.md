# Lembar Validasi Sprint Report 4 — Bagian B: Sprint Review

| | |
|---|---|
| Sprint | : Sprint 4 |
| Periode Sprint | : 13 – 19 November 2026 |
| Tanggal *Sprint Review* | : 19 November 2026 |
| *Product Owner* (validator) | : Dosen Koordinator PKL Prodi PTIK UNJ |
| Scrum Master | : Dosen pembimbing |
| Developer | : Deni Merdiansyah (NIM {{NIM_DEVELOPER}}) |

## Tujuan

Lembar ini memuat hasil *Sprint Review* Sprint 4, yaitu Increment yang dihasilkan, untuk diperiksa dan divalidasi terhadap *Sprint Goal* dan kriteria selesai yang ditetapkan pada *Sprint Planning*.

## *Sprint Goal*

Menghasilkan website Pekael yang dapat dipakai secara lokal: mahasiswa dapat mengetik pertanyaan dan menerima jawaban beserta rujukan halaman buku panduan melalui tampilan yang sederhana dan mudah dipahami, admin dapat masuk dengan satu akun lalu memperbarui buku panduan tanpa menghilangkan knowledge base yang sedang dipakai, dan seluruh fungsi diuji sebelum validasi ahli pada Sprint 5.

Status pencapaian: ☑ Tercapai ☐ Tercapai sebagian ☐ Tidak tercapai

## Increment yang dihasilkan

| No | Increment | Kriteria selesai | Hasil | Bukti |
|---|---|---|---|---|
| 1 | Halaman tanya-jawab mahasiswa | Pertanyaan dapat dikirim, tanda proses tampil, jawaban tampil bersama nama dokumen dan halaman PDF dari potongan yang benar-benar diambil, pertanyaan di luar cakupan dan gangguan layanan menampilkan pesan yang jelas, tampilan dapat dipakai di laptop dan ponsel | Website bertema navy dengan perkenalan "PKL, kalau dibaca jadi pe·ka·el", contoh pertanyaan, dan fakta singkat PKL beserta halamannya. Pertanyaan tampil di kanan dan jawaban di kiri seperti aplikasi percakapan, lengkap dengan jam, penanda halaman, dan kutipan. Tanda proses mengikuti langkah yang sedang berjalan. Jawaban menyesuaikan gaya penanya (santai atau formal), disajikan dengan bentuk yang bervariasi, dan isinya tetap sesuai buku. Pertanyaan yang jawabannya tidak ada di buku diarahkan dengan ramah ke Koordinator PKL, Admin Prodi PTIK, atau Koordinator Program Studi. Sapaan dan ucapan terima kasih dibalas seperti percakapan biasa. Tampilan diperiksa pada ukuran laptop dan ponsel | Logbook 13–19 November, catatan percobaan EXP-006 sampai EXP-009 |
| 2 | Halaman admin | Hanya satu akun admin dari pengaturan yang dapat masuk, admin dapat mengganti buku panduan, laporan pembangunan tampil, dan knowledge base lama tetap dipakai bila pembangunan gagal | Ruang admin di alamat terpisah dengan halaman masuk berbentuk kartu pengelola. Akun dibaca dari pengaturan lokal, salah kata sandi lima kali mengunci formulir 30 detik. Admin dapat melihat ringkasan buku dan peta halaman, mengganti atau membangun ulang buku dengan tanda proses dan laporan, mengaktifkan kembali versi sebelumnya, menguji pertanyaan, dan melihat pengaturan tanpa kata sandi atau API key. Pembangunan yang gagal tidak mengganti knowledge base yang dipakai mahasiswa | Logbook 16 November, pengujian otomatis ruang admin |

## Hasil pengujian

| Jenis pengujian | Cakupan | Hasil |
|---|---|---|
| Pengujian otomatis | Halaman mahasiswa, ruang admin, simpanan jawaban, gaya bahasa, respons arahan, serta seluruh komponen sebelumnya | 327 lulus, 0 gagal |
| Uji 44 pertanyaan (EXP-009) | 36 pertanyaan dalam cakupan, 5 pertanyaan PKL yang jawabannya tidak ada di buku, 3 pertanyaan di luar topik PKL | 35 dari 36 dijawab dengan rujukan halaman, 5 dari 5 diarahkan ke pihak yang tepat, 3 dari 3 dibalas sebagai percakapan, tanpa kalimat penolakan |
| Uji gaya bahasa | Pasangan pertanyaan santai dan formal untuk topik yang sama | Isi jawaban sama, gaya bahasa mengikuti penanya |
| Uji tampilan | Tangkapan layar ukuran laptop dan ponsel | Intro, halaman awal, tanda proses, percakapan, dan ruang admin tampil sesuai rancangan |
| Waktu persiapan | Dari Pekael dijalankan sampai siap menjawab | Sekitar 20 detik menjadi sekitar 7 detik, di website berlangsung selama intro |
| Waktu jawab | Uji 44 pertanyaan | Bergantung pada kondisi layanan Gemini: median 2,8 detik pada 18 November dan 5,4 detik pada 19 November |

## Pekerjaan yang belum selesai

| Pekerjaan | Alasan | Tindak lanjut |
|---|---|---|
| Pemeriksaan ulang label halaman daftar topik dan penambahan contoh pertanyaan halaman 22–28 (S4-T01) | Waktu sprint dipakai untuk menindaklanjuti masukan *Product Owner* dan dosen pembimbing tentang gaya jawaban | Dibawa ke Sprint 5 bersama penyusunan dataset evaluasi |

## Masukan *Product Owner*

........................................................................................................................

........................................................................................................................

## Perubahan Product Backlog

| Perubahan | Alasan |
|---|---|
| Respons arahan yang ramah dan bervariasi untuk pertanyaan yang jawabannya tidak ada di buku pedoman | Masukan *Product Owner* pada bimbingan 17 November 2026 |
| Gaya jawaban yang menyesuaikan penanya dan bentuk penyajian yang bervariasi | Masukan dosen pembimbing |
| Pengelolaan beberapa dokumen knowledge base di ruang admin, untuk dokumen tambahan dari *Product Owner* | Rencana penambahan knowledge base khusus dari *Product Owner* |
| Sprint 4–6 masing-masing 1 minggu | Keputusan pemilik pada 17 November 2026 |

## Pernyataan validasi

Berdasarkan pemeriksaan terhadap Increment Sprint 4 pada lembar ini, *Product Owner* menyatakan Increment tersebut:

☑ Diterima
☐ Diterima dengan catatan: ........................................................................
☐ Belum diterima, pekerjaan dikembalikan ke Product Backlog

| | |
|---|---|
| Jakarta, 19 November 2026<br>Scrum Master,<br><br><br><br>Nur Elah, S.Kom., M.T<br>NIP. {{NIP_SCRUM_MASTER_REVIEW}} | <br>Developer,<br><br><br><br>Deni Merdiansyah<br>NIM {{NIM_DEVELOPER}} |

*Dasar penyusunan: Schwaber & Sutherland (2020) untuk komponen Sprint Review. Rujukan lengkap tercantum pada laporan.*
