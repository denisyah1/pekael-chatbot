# Lembar Pemeriksaan Hasil OCR — Sprint 1

| | |
|---|---|
| Dokumen | : Buku Pedoman Praktik Kerja Lapangan UNJ 2025 (29 halaman, seluruhnya hasil pemindaian) |
| Halaman diperiksa | : 4 – 16 (halaman yang diusulkan masuk knowledge base) |
| Tanggal pemeriksaan | : 26 Oktober 2026 |
| Pemeriksa tahap pertama | : Claude Code (asisten AI), membandingkan gambar halaman dengan teks hasil OCR |
| Verifikasi akhir | : Deni Merdiansyah (Developer) |

## Tujuan

Lembar ini mencatat hasil pemeriksaan teks hasil OCR terhadap dokumen asli, sesuai tugas 3 pada *Sprint Planning* (memverifikasi dan membersihkan teks hasil OCR). Pemeriksaan difokuskan pada angka, tanggal, daftar, persyaratan, dan istilah penting.

## Cara pemeriksaan

1. Setiap halaman ditampilkan sebagai gambar, lalu dibandingkan kata demi kata dengan teks hasil OCR.
2. Kesalahan OCR dicatat dan diperbaiki dalam file koreksi per halaman. File koreksi dipakai otomatis setiap kali knowledge base dibangun ulang.
3. Salah ketik yang memang ada di dokumen asli **tidak diubah**, agar teks tetap setia pada sumber. Contoh: "Mengkoordininasikan" (hal. 8), "disesuikan" (hal. 10).
4. Bagan dan tabel yang tidak dapat dibaca OCR ditulis ulang secara manual sesuai gambar asli.

## Ringkasan hasil

| Hasil | Jumlah halaman | Halaman |
|---|---|---|
| Benar seluruhnya, tanpa koreksi | 4 | 7, 9, 12, 15 |
| Koreksi kecil (huruf, tanda baca, spasi) | 6 | 4, 5, 6, 8, 10, 11 |
| Bagan atau tabel ditulis ulang manual | 3 | 13, 14, 16 |

Semua angka dan ketentuan penting terbaca benar oleh OCR: masa PKL minimal 4 bulan, syarat minimal 100 SKS, nilai kelulusan minimal B+, bobot 170 menit per SKS, PKL berjumlah 6 SKS, serta nomor-nomor peraturan.

## Rincian temuan dan koreksi

| Hal. | Isi halaman | Temuan OCR | Koreksi | Diverifikasi |
|---|---|---|---|---|
| 4 | Latar belakang | "BABI" | "BAB I" | ☐ |
| 5 | Latar belakang, pengertian, tujuan PKL | "/ard-skill" (huruf miring salah dibaca), subjudul "Cc.", "4.Mengembangkan" | "hard-skill", "C.", "4. Mengembangkan" | ☐ |
| 6 | Manfaat PKL | "c.Memperoleh" (tanpa spasi) | "c. Memperoleh" | ☐ |
| 7 | Waktu dan tempat pelaksanaan | Tidak ada | — | ☐ |
| 8 | Tugas koordinator prodi dan koordinator PKL | Penanda butir "c." terbaca "€" dan tergabung dengan butir b | Butir c dipisah kembali | ☐ |
| 9 | Tugas dosen pembimbing, mitra, mentor, mahasiswa | Tidak ada | — | ☐ |
| 10 | Kewajiban mahasiswa, persyaratan peserta | "sesaina", butir "l." terbaca "1.", "Gika", "masing- masing" | "sesama", "l.", "(jika", "masing-masing" | ☐ |
| 11 | Syarat kelulusan, tata tertib | Titik di akhir butir terbaca koma | Diganti titik | ☐ |
| 12 | Standar operasional prosedur | Tidak ada | — | ☐ |
| 13 | Prosedur administrasi pengajuan PKL | **Bagan 2.1 Prosedur Pengajuan PKL terbaca acak** | Ditulis ulang sebagai 7 tahapan berurutan | ☐ |
| 14 | Prosedur pelaksanaan, sanksi | **Bagan 2.2 Prosedur Pelaksanaan PKL terbaca acak**, subjudul "Cc.", "1," | Ditulis ulang sebagai 6 tahapan berurutan, "C.", "1." | ☐ |
| 15 | Sanksi | Tidak ada | — | ☐ |
| 16 | Sistem penilaian | **Tabel konversi nilai hampir hilang seluruhnya**, "BAB II", "(nstrumen", "(1-5)" terpotong | Tabel 10 baris ditulis ulang, "BAB III", "(Instrumen", "(1-5)" | ☐ |

## Isi yang ditulis ulang manual

**Bagan 2.1 Prosedur Pengajuan PKL (hal. 13):** 1) Pemenuhan persyaratan umum, 2) Pendaftaran online di SIAKAD, 3) Penentuan kelompok, lembaga, dospem, 4) Penyusunan proposal dan CV, 5) Pembuatan surat permohonan PKL, 6) Mahasiswa proaktif, 7) Pelaksanaan PKL.

**Bagan 2.2 Prosedur Pelaksanaan PKL (hal. 14):** 1) Survey, 2) Bertemu pamong, 3) Buat perencanaan, 4) Lapor dosen pembimbing, 5) Konfirmasi & kesepakatan, 6) Penyusunan laporan.

**Tabel nilai akhir (hal. 16):**

| Tingkat Penguasaan | Nilai | Bobot |
|---|---|---|
| 86-100 | A | 4 |
| 81-85 | A- | 3,7 |
| 76-80 | B+ | 3,3 |
| 71-75 | B | 3,0 |
| 66-70 | B- | 2,7 |
| 61-65 | C+ | 2,3 |
| 56-60 | C | 2,0 |
| 51-55 | C- | 1,7 |
| 46-50 | D | 1 |
| 0-45 | E | 0 |

## Halaman di luar pemeriksaan ini

| Halaman | Alasan |
|---|---|
| 1–3, 17–26, 29 | Diusulkan dikecualikan dari knowledge base (lihat [Usulan Penyaringan](usulan_penyaringan.md)). Diperiksa hanya bila Product Owner memutuskan halaman tersebut dipakai. |
| 27–28 | Lampiran instrumen penilaian (tabel), menunggu keputusan Product Owner. Bila dipakai, tabel harus ditulis ulang manual seperti halaman 16. |

## Pernyataan verifikasi

Saya telah membandingkan koreksi pada lembar ini dengan dokumen asli dan menyatakan teks hasil OCR halaman 4 – 16 telah terverifikasi.

| | |
|---|---|
| Jakarta, ...........................<br>Developer,<br><br><br><br>Deni Merdiansyah<br>NIM {{NIM_DEVELOPER}} | |
