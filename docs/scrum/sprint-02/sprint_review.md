# Lembar Validasi Sprint Report 2 — Bagian B: Sprint Review

| | |
|---|---|
| Sprint | : Sprint 2 |
| Periode Sprint | : 30 Oktober – 5 November 2026 |
| Tanggal *Sprint Review* | : 5 November 2026 |
| *Product Owner* (validator) | : Dosen Koordinator PKL Prodi PTIK UNJ |
| Scrum Master | : Dosen pembimbing |
| Developer | : Deni Merdiansyah (NIM {{NIM_DEVELOPER}}) |

## Tujuan

Lembar ini memuat hasil *Sprint Review* Sprint 2, yaitu Increment yang dihasilkan, untuk diperiksa dan divalidasi oleh *Product Owner* terhadap *Sprint Goal* dan kriteria selesai yang ditetapkan pada *Sprint Planning*.

## *Sprint Goal*

Mengubah teks buku panduan PKL yang telah disaring menjadi potongan teks (*chunk*) yang tetap membawa keterangan sumber dan halaman, lalu menjadi representasi vektor menggunakan model embedding Gemini, dengan ukuran potongan awal yang dipilih berdasarkan percobaan, sebagai dasar penyimpanan FAISS dan alur tanya-jawab pada Sprint 3.

Status pencapaian: ☐ Tercapai ☐ Tercapai sebagian ☐ Tidak tercapai

## Increment yang dihasilkan

| No | Increment | Kriteria selesai | Hasil | Bukti |
|---|---|---|---|---|
| 1 | Potongan teks berlabel sumber | Setiap potongan menyimpan nama dokumen, halaman PDF, bagian, dan nomor unik, hanya berasal dari halaman yang disetujui *Product Owner* | Halaman 4–16 menghasilkan 26 potongan. Setiap potongan membawa nama dokumen, halaman PDF, judul bab atau subbab, dan nomor unik. Potongan tidak pernah melewati batas halaman, sehingga rujukan halaman tetap tepat. Halaman yang dipakai dapat diubah lewat pengaturan sesuai keputusan *Product Owner* | Laporan potongan, pengujian otomatis |
| 2 | Vektor embedding dan parameter awal | Semua potongan dan pertanyaan menghasilkan vektor berukuran sama, percobaan ukuran potongan tercatat beserta alasan pemilihan parameter awal | Semua vektor berukuran 768 angka dan disamakan panjangnya. Percobaan dengan 30 contoh pertanyaan: 29 pertanyaan menemukan halaman yang tepat di empat hasil teratas pada semua ukuran potongan. Ukuran awal 1.000 karakter dengan tumpang tindih 150 dipertahankan karena perbedaan antarukuran hanya satu pertanyaan | Catatan percobaan EXP-002 |
| 3 | Teks hasil OCR terverifikasi (bawaan Sprint 1) | Koreksi OCR halaman 4–16 dibandingkan dengan buku asli | Developer memverifikasi koreksi dan menyatakannya akurat tanpa perubahan | Lembar Pemeriksaan Hasil OCR Sprint 1 |

## Hasil pengujian

| Jenis pengujian | Cakupan | Hasil |
|---|---|---|
| Pengujian otomatis | Pemilihan halaman, pemotong teks, penghubung embedding, dan seluruh komponen sebelumnya | 143 lulus, 0 gagal |
| Uji langsung layanan Gemini | Pembuatan vektor untuk potongan dan pertanyaan, batas panjang teks | Berhasil, vektor 768 angka. Teks sangat panjang ternyata dipotong diam-diam oleh layanan, sehingga sistem kini menolaknya |
| Percobaan ukuran potongan (EXP-002) | 4 ukuran potongan, 2 ukuran vektor, 30 pertanyaan dalam cakupan dan 8 di luar cakupan | 29 dari 30 pertanyaan menemukan halaman yang tepat. Layanan sempat sibuk dua kali dan sistem berhasil mencoba ulang |

## Pekerjaan yang belum selesai

| Pekerjaan | Alasan | Tindak lanjut |
|---|---|---|
| Keputusan *Product Owner* atas halaman knowledge base dan bentuk hasil penyaringan (S2-T02) | Pertemuan dengan *Product Owner* belum terlaksana | Diputuskan pada *Sprint Review* ini |
| Usulan Developer menambahkan halaman 22–25 (sistematika laporan PKL) | Termasuk perubahan ruang lingkup proposal, perlu persetujuan *Product Owner* | Diputuskan pada *Sprint Review* ini. Bila disetujui, hasil OCR halaman tersebut diperiksa pada awal Sprint 3 |

## Masukan *Product Owner*

........................................................................................................................

........................................................................................................................

## Perubahan Product Backlog

| Perubahan | Alasan |
|---|---|
| Menambahkan instruksi kepada Gemini untuk menyatakan "informasi tidak ditemukan" pada Sprint 3 | Percobaan menunjukkan pertanyaan PKL yang jawabannya tidak ada di buku (misalnya jadwal pendaftaran) tidak dapat ditolak hanya dengan pencarian |
| Memakai hasil jarak pencarian dari percobaan sebagai titik awal kalibrasi batas relevansi pada Sprint 3 | Pertanyaan di luar topik PKL sudah terlihat jauh berbeda dari pertanyaan PKL |
| Keputusan ruang lingkup halaman 22–25 dicatat sebagai perubahan Product Backlog bila disetujui | Menjaga batasan penelitian tetap tertelusur |

## Pernyataan validasi

Berdasarkan pemeriksaan terhadap Increment Sprint 2 pada lembar ini, *Product Owner* menyatakan Increment tersebut:

☐ Diterima
☐ Diterima dengan catatan: ........................................................................
☐ Belum diterima, pekerjaan dikembalikan ke Product Backlog

| | |
|---|---|
| Jakarta, 5 November 2026<br>*Product Owner* (Dosen Koordinator PKL),<br><br><br><br>Bambang Satrio, S. Pd., M. Kom.<br>NIP. {{NIP_PRODUCT_OWNER}} | <br>Developer,<br><br><br><br>Deni Merdiansyah<br>NIM {{NIM_DEVELOPER}} |

*Dasar penyusunan: Schwaber & Sutherland (2020) untuk komponen Sprint Review. Rujukan lengkap tercantum pada laporan.*
