# Lembar Validasi Sprint Report 1 — Bagian A: Sprint Planning

| | |
|---|---|
| Sprint | : Sprint 1 (minggu ke-1 sampai ke-2) |
| Periode Sprint | : 23 – 29 Oktober 2026 |
| *Product Owner* (validator) | : Dosen Koordinator PKL Prodi PTIK UNJ |
| Scrum Master | : Dosen pembimbing |
| Developer | : Deni Merdiansyah (NIM {{NIM_DEVELOPER}}) |

## Tujuan

Lembar ini memuat hasil *Sprint Planning* Sprint 1 untuk divalidasi oleh *Product Owner* dari sisi kebutuhan informasi PKL dan urutan pengerjaan, sebelum Sprint 1 dikerjakan. Sesuai Scrum Guide, *Sprint backlog* terdiri atas *Sprint Goal*, Product Backlog Item yang dipilih untuk Sprint, dan rencana pengerjaannya, ketiganya disajikan pada bagian 2 sampai 4.

## *Sprint Goal*

Menyiapkan teks buku panduan PKL yang telah diekstraksi dan diverifikasi, serta knowledge base yang telah disaring sesuai lingkup Prodi PTIK, sebagai dasar tahap text splitting dan embedding pada Sprint 2.

## Product Backlog Item yang dipilih

| No | Product Backlog Item | Prioritas | Alasan dipilih pada Sprint 1 |
|---|---|---|---|
| 1 | Ekstraksi teks dari dokumen panduan PKL hasil pemindaian melalui OCR | Tinggi | Menjadi prasyarat seluruh tahap berikutnya karena menyediakan teks yang dapat diproses |
| 2 | Penyaringan dan pengerucutan konten dokumen agar relevan dengan lingkup Prodi PTIK | Tinggi | Menentukan isi knowledge base, memerlukan validasi *Product Owner* atas relevansi buku panduan |

## Rencana pengerjaan (*Sprint backlog*)

| | |
|---|---|
| Dokumen sumber | : Buku Panduan PKL tingkat universitas versi 2025, berupa hasil pemindaian, diunggah pada laman ft.unj.ac.id (April 2026) |
| Lingkup penyaringan | : Prodi PTIK, Fakultas Teknik, Universitas Negeri Jakarta |
| Alat | : Tesseract OCR, keluaran berupa teks yang dapat diproses |

| No | Tugas | PBI terkait | Keluaran | Waktu |
|---|---|---|---|---|
| 1 | Menyiapkan salinan buku panduan PKL dan memastikan keterbacaan hasil pemindaian | 1 | Berkas sumber siap diproses | Minggu 1 |
| 2 | Mengekstraksi teks dari buku panduan menggunakan Tesseract OCR | 1 | Teks hasil OCR mentah | Minggu 1 |
| 3 | Memverifikasi dan membersihkan teks hasil OCR (koreksi karakter yang keliru) | 1 | Teks hasil OCR terverifikasi | Minggu 1 sampai 2 |
| 4 | Menyaring dan mengerucutkan konten sesuai lingkup Prodi PTIK | 2 | Knowledge base tersaring | Minggu 2 |
| 5 | Menyusun daftar bagian yang dipertahankan dan yang dikeluarkan beserta alasannya | 2 | Daftar penyaringan untuk validasi *Product Owner* | Minggu 2 |

## Increment dan kriteria selesai

| Increment | Kriteria selesai | Titik validasi |
|---|---|---|
| Teks hasil OCR terverifikasi | Seluruh halaman yang digunakan telah diekstraksi dan diperiksa terhadap dokumen asli, kesalahan karakter pada istilah dan angka penting telah dikoreksi | Peneliti memeriksa, dikonfirmasi pada Sprint Review |
| Knowledge base tersaring | Bagian buku panduan yang relevan dengan PTIK telah dipilih, bagian yang dikeluarkan tercatat beserta alasannya | Validasi *Product Owner* atas relevansi buku panduan |

## Peran dan keterlibatan pada Sprint 1

| Peran | Pemegang | Keterlibatan | Keluaran |
|---|---|---|---|
| *Product Owner* | Dosen koordinator PKL | Memvalidasi kebutuhan dan urutan pada *Sprint Planning*, memvalidasi isi Increment pada *Sprint Review* | Bukti validasi |
| Scrum Master | Dosen pembimbing | Memastikan *Sprint Planning*, *Sprint Review*, dan *Sprint Retrospective* terlaksana, mengonfirmasi checklist akhir Sprint | Konfirmasi checklist |
| Developers | Peneliti | Mengerjakan *Sprint backlog* dan mengisi logbook setiap hari kerja aktif | Logbook, Increment |

## Jadwal peristiwa Sprint 1

| Peristiwa | Waktu | Pelaksana |
|---|---|---|
| *Sprint Planning* | 23 Oktober 2026 | Peneliti, *Product Owner* |
| Pengerjaan harian (logbook) | 23 – 29 Oktober 2026 | Peneliti |
| *Sprint Review* | 29 Oktober 2026 | Peneliti, *Product Owner*, Scrum Master |
| *Sprint Retrospective* | 29 Oktober 2026 | Peneliti, Scrum Master |

## Risiko dan penanganan

| Risiko | Dampak | Penanganan |
|---|---|---|
| Kualitas pindaian rendah sehingga hasil OCR banyak mengandung kesalahan karakter | Teks tidak akurat dan memengaruhi tahap berikutnya | Verifikasi dan pembersihan manual terhadap dokumen asli (tugas 3) |
| Buku panduan memuat bagian yang tidak berlaku untuk PTIK | Knowledge base memuat informasi yang keliru | Daftar penyaringan divalidasi *Product Owner* (tugas 5) |

## Pernyataan validasi

Berdasarkan kebutuhan informasi PKL di Prodi PTIK, *Sprint Planning* Sprint 1 pada lembar ini, yaitu *Sprint Goal*, *Product Backlog Item* yang dipilih, rencana pengerjaan, serta Increment yang diharapkan, telah divalidasi dan dapat dilaksanakan.

| | |
|---|---|
| Jakarta, 23 Oktober 2026<br>*Product Owner* (Dosen Koordinator PKL),<br><br><br><br>Bambang Satrio, S. Pd., M. Kom.<br>NIP. {{NIP_PRODUCT_OWNER}} | <br>Developer,<br><br><br><br>Deni Merdiansyah<br>NIM {{NIM_DEVELOPER}} |

*Dasar penyusunan: Schwaber & Sutherland (2020) untuk komponen Sprint Planning, Liu et al. (2019) dan Verwijs & Russo (2023) untuk peran perencanaan Sprint yang jelas dan umpan balik pemangku kepentingan. Rujukan lengkap tercantum pada laporan.*
