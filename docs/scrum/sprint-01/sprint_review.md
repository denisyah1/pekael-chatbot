# Lembar Validasi Sprint Report 1 — Bagian B: Sprint Review

| | |
|---|---|
| Sprint | : Sprint 1 |
| Periode Sprint | : 23 – 29 Oktober 2026 |
| Tanggal *Sprint Review* | : 29 Oktober 2026 |
| *Product Owner* (validator) | : Dosen Koordinator PKL Prodi PTIK UNJ |
| Scrum Master | : Dosen pembimbing |
| Developer | : Deni Merdiansyah (NIM {{NIM_DEVELOPER}}) |

## Tujuan

Lembar ini memuat hasil *Sprint Review* Sprint 1, yaitu Increment yang dihasilkan, untuk diperiksa dan divalidasi oleh *Product Owner* terhadap *Sprint Goal* dan kriteria selesai yang ditetapkan pada *Sprint Planning*.

## *Sprint Goal*

Menyiapkan teks buku panduan PKL yang telah diekstraksi dan diverifikasi, serta knowledge base yang telah disaring sesuai lingkup Prodi PTIK, sebagai dasar tahap text splitting dan embedding pada Sprint 2.

Status pencapaian: ☐ Tercapai ☐ Tercapai sebagian ☐ Tidak tercapai

## Increment yang dihasilkan

| No | Increment | Kriteria selesai | Hasil | Bukti |
|---|---|---|---|---|
| 1 | Teks hasil OCR terverifikasi | Seluruh halaman yang digunakan telah diekstraksi dan diperiksa terhadap dokumen asli, kesalahan karakter pada istilah dan angka penting telah dikoreksi | Ke-29 halaman berhasil dibaca dengan OCR (rata-rata keyakinan sekitar 90%). Halaman 4–16 diperiksa kata demi kata: 4 halaman benar seluruhnya, 6 halaman dikoreksi kecil, 2 bagan prosedur dan 1 tabel nilai ditulis ulang manual. Semua angka penting terbaca benar | Lembar Pemeriksaan Hasil OCR, laporan ekstraksi |
| 2 | Knowledge base tersaring | Bagian buku panduan yang relevan dengan PTIK telah dipilih, bagian yang dikeluarkan tercatat beserta alasannya | Usulan: halaman 4–16 (prosedur, persyaratan, tahapan, penilaian) dipakai, halaman 1–3, 17–26, dan 29 dikeluarkan beserta alasannya. Halaman 27–28 (lampiran penilaian) menunggu keputusan | Usulan Penyaringan Isi Buku Pedoman |
| 3 | Daftar topik pertanyaan mahasiswa (tambahan) | Topik disusun dari isi buku panduan sebagai dasar dataset evaluasi dan UAT | 30 topik dengan contoh pertanyaan dan halaman sumber, ditambah contoh pertanyaan di luar cakupan | Daftar Topik Pertanyaan Mahasiswa |

## Hasil pengujian

| Jenis pengujian | Cakupan | Hasil |
|---|---|---|
| Pengujian otomatis | Pembaca PDF, OCR, perapian teks, koreksi manual, konfigurasi, ekspor dokumen | 105 lulus, 0 gagal |
| Uji coba alat (smoke test) | Penyimpanan vektor, pembaca PDF, OCR bahasa Indonesia, layanan Gemini | Berhasil |
| Pemeriksaan manual | Teks hasil OCR halaman 4–16 terhadap dokumen asli | Selesai, menunggu verifikasi akhir peneliti |

## Pekerjaan yang belum selesai

| Pekerjaan | Alasan | Tindak lanjut |
|---|---|---|
| Verifikasi akhir koreksi OCR oleh peneliti | Menunggu pemeriksaan ulang terhadap buku asli | Diselesaikan sebelum Sprint 2 berjalan |
| Keputusan penyaringan dan bentuk hasilnya (PDF baru atau daftar halaman) | Memerlukan keputusan *Product Owner* | Diputuskan pada *Sprint Review* ini |
| Lampiran penilaian halaman 27–28 | Menunggu keputusan dipakai atau tidak. Jika dipakai, tabel perlu ditulis ulang manual | Dikerjakan di awal Sprint 2 bila dipakai |

## Masukan *Product Owner*

........................................................................................................................

........................................................................................................................

## Perubahan Product Backlog

| Perubahan | Alasan |
|---|---|
| Menambahkan pekerjaan pemilihan halaman knowledge base ke awal Sprint 2 | Hanya halaman yang disetujui *Product Owner* yang boleh dipakai chatbot |
| Menambahkan keterangan bagian (judul bab/subbab) pada setiap potongan teks di Sprint 2 | Memperjelas rujukan sumber pada jawaban chatbot |
| Rujukan sumber memakai istilah "halaman PDF" | Buku panduan tidak mencetak nomor halaman |

## Pernyataan validasi

Berdasarkan pemeriksaan terhadap Increment Sprint 1 pada lembar ini, *Product Owner* menyatakan Increment tersebut:

☐ Diterima
☐ Diterima dengan catatan: ........................................................................
☐ Belum diterima, pekerjaan dikembalikan ke Product Backlog

| | |
|---|---|
| Jakarta, 29 Oktober 2026<br>*Product Owner* (Dosen Koordinator PKL),<br><br><br><br>Bambang Satrio, S. Pd., M. Kom.<br>NIP. {{NIP_PRODUCT_OWNER}} | <br>Developer,<br><br><br><br>Deni Merdiansyah<br>NIM {{NIM_DEVELOPER}} |

*Dasar penyusunan: Schwaber & Sutherland (2020) untuk komponen Sprint Review. Rujukan lengkap tercantum pada laporan.*
