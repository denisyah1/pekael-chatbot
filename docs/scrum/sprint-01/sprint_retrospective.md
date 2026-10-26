# Lembar Validasi Sprint Report 1 — Bagian C: Sprint Retrospective

| | |
|---|---|
| Sprint | : Sprint 1 |
| Periode Sprint | : 23 – 29 Oktober 2026 |
| Tanggal *Sprint Retrospective* | : 29 Oktober 2026 |
| Scrum Master | : Dosen pembimbing |
| Developer | : Deni Merdiansyah (NIM {{NIM_DEVELOPER}}) |

## Tujuan

Lembar ini memuat hasil *Sprint Retrospective* Sprint 1, yaitu evaluasi cara kerja selama sprint dan rencana perbaikan untuk sprint berikutnya, untuk dikonfirmasi oleh Scrum Master.

## Yang berjalan baik

- Persiapan lingkungan kerja diselesaikan di awal, sehingga sprint bisa langsung fokus pada pengolahan buku panduan.
- Kualitas pindaian buku panduan baik, sehingga teks paragraf dan seluruh angka penting terbaca benar oleh OCR.
- Tingkat keyakinan OCR per halaman membantu menentukan halaman yang perlu diperiksa lebih dulu.
- Koreksi hasil OCR disimpan per halaman dan dipakai otomatis, sehingga tidak perlu diulang setiap kali teks dibangun ulang.
- Dokumen sprint dapat dicetak ke Word dan PDF dengan format seragam dalam satu langkah.

## Yang perlu diperbaiki

- Format dokumen validasi baru diseragamkan di tengah sprint, sehingga beberapa dokumen perlu disusun ulang. Format sebaiknya disepakati sejak *Sprint Planning*.
- Satuan waktu pada rencana pengerjaan masih memakai "minggu 1 sampai 2", padahal Sprint 1 hanya berlangsung satu minggu. Rencana berikutnya perlu memakai tanggal.
- Keputusan *Product Owner* tentang penyaringan isi baru diambil di akhir sprint. Keputusan seperti ini sebaiknya dijadwalkan di pertengahan sprint.

## Hambatan dan penyebab

| Hambatan | Penyebab | Dampak pada sprint |
|---|---|---|
| Bagan alur dan tabel tidak terbaca OCR | OCR hanya andal untuk teks berbentuk paragraf dan daftar | Perlu penulisan ulang manual dan verifikasi tambahan |
| API key sempat tertulis di file contoh dan masuk catatan perubahan lokal | Kekeliruan pengisian file pengaturan | Terdeteksi sebelum terunggah ke publik. Dipasang pemeriksa otomatis agar tidak terulang |
| Server Gemini sempat sibuk saat uji coba | Lonjakan permintaan di sisi penyedia layanan | Berhasil pada percobaan kedua. Menjadi catatan untuk penanganan gangguan di Sprint 3 |

## Rencana perbaikan untuk Sprint 2

| Tindakan | Penanggung jawab | Diperiksa pada |
|---|---|---|
| Menulis waktu rencana pengerjaan dalam bentuk tanggal | Developer | *Sprint Planning* Sprint 2 |
| Menjadwalkan validasi *Product Owner* di pertengahan sprint, bukan hanya di akhir | Developer, Scrum Master | *Sprint Review* Sprint 2 |
| Memakai templat dokumen sprint yang sudah disepakati sejak awal sprint | Developer | *Sprint Review* Sprint 2 |
| Menjalankan pemeriksa API key sebelum setiap penyimpanan perubahan | Developer | *Sprint Review* Sprint 2 |

## Tindak lanjut rencana perbaikan sprint sebelumnya

Tidak ada, Sprint 1 adalah sprint pertama.

## Checklist akhir Sprint

| Butir | Status |
|---|---|
| *Sprint Planning* terlaksana dan divalidasi *Product Owner* | ☐ |
| Logbook diisi setiap hari kerja aktif | ☐ |
| *Sprint Review* terlaksana dan Increment divalidasi *Product Owner* | ☐ |
| *Sprint Retrospective* terlaksana | ☐ |
| Product Backlog diperbarui | ☐ |

## Konfirmasi Scrum Master

Berdasarkan checklist di atas, peristiwa Scrum pada Sprint 1 telah terlaksana sesuai rencana.

| | |
|---|---|
| Jakarta, 29 Oktober 2026<br>Scrum Master,<br><br><br><br>Dr. Widodo, M. Kom. | <br>Developer,<br><br><br><br>Deni Merdiansyah<br>NIM {{NIM_DEVELOPER}} |

*Dasar penyusunan: Schwaber & Sutherland (2020) untuk komponen Sprint Retrospective. Rujukan lengkap tercantum pada laporan.*
