# Lembar Validasi Sprint Report 4 — Bagian C: Sprint Retrospective

| | |
|---|---|
| Sprint | : Sprint 4 |
| Periode Sprint | : 13 – 19 November 2026 |
| Tanggal *Sprint Retrospective* | : 19 November 2026 |
| Scrum Master | : Dosen pembimbing |
| Developer | : Deni Merdiansyah (NIM {{NIM_DEVELOPER}}) |

## Tujuan

Lembar ini memuat hasil *Sprint Retrospective* Sprint 4, yaitu evaluasi cara kerja selama sprint dan rencana perbaikan untuk sprint berikutnya, untuk dikonfirmasi oleh Scrum Master.

## Yang berjalan baik

- Tampilan dievaluasi Developer hampir setiap hari, sehingga masukan langsung diterapkan dan diperiksa melalui tangkapan layar ukuran laptop dan ponsel.
- Masukan *Product Owner* dan dosen pembimbing dari bimbingan langsung ditindaklanjuti di sprint yang sama.
- Setiap perubahan gaya jawaban diuji ulang dengan 44 contoh pertanyaan, sehingga kesalahan akibat perubahan instruksi segera ketahuan, misalnya jawaban "lulus" yang keliru dan pertanyaan yang tiba-tiba tidak terjawab.
- Penyebab waktu tunggu diukur lebih dulu sebelum diperbaiki, sehingga perbaikan tepat sasaran (waktu persiapan turun dari sekitar 20 detik menjadi sekitar 7 detik).
- Kata sandi admin tetap disimpan di luar repository walaupun diminta ditulis di kode, karena repository bersifat publik.

## Yang perlu diperbaiki

- Perubahan instruksi untuk gaya bahasa beberapa kali menurunkan ketepatan jawaban. Setiap perubahan instruksi perlu langsung diuji dengan seluruh contoh pertanyaan sebelum dicoba di website.
- Pemeriksaan ulang label daftar topik kembali tertunda dua sprint berturut-turut.
- Pengujian waktu masuk dari intro di website belum dapat dilakukan langsung oleh Developer pada sprint ini.

## Hambatan dan penyebab

| Hambatan | Penyebab | Dampak pada sprint |
|---|---|---|
| Waktu jawab berubah-ubah (median 2,8 detik pada satu hari, 5,4 detik pada hari berikutnya) | Kondisi layanan Gemini versi gratis | Waktu jawab belum stabil di bawah 5 detik |
| Gemini kadang salah menulis penanda khusus atau mengabaikan petunjuk gaya | Kemampuan model versi ringan | Diperlukan pemeriksaan tambahan dalam kode |
| Login admin sempat ditolak di komputer Developer | Isian otomatis browser | Waktu penelusuran, diperbaiki dengan mematikan isian otomatis |

## Rencana perbaikan untuk Sprint 5

| Tindakan | Penanggung jawab | Diperiksa pada |
|---|---|---|
| Menjalankan uji 44 contoh pertanyaan setiap kali instruksi Gemini diubah, sebelum perubahan dipakai | Developer | *Sprint Review* Sprint 5 |
| Menyelesaikan pemeriksaan label daftar topik bersama penyusunan dataset evaluasi pada awal sprint | Developer | *Sprint Review* Sprint 5 |
| Mengukur waktu jawab pada beberapa waktu berbeda (pagi, siang, malam) sebagai bahan keputusan model berbayar | Developer | *Sprint Review* Sprint 5 |

## Tindak lanjut rencana perbaikan Sprint 3

| Tindakan | Terlaksana | Catatan |
|---|---|---|
| Menjadwalkan pemeriksaan hasil kerja yang memerlukan Developer atau *Product Owner* pada hari pertama sprint | ☑ | Evaluasi tampilan oleh Developer dimulai sejak hari kedua dan dilakukan hampir setiap hari |
| Memeriksa ulang label halaman pada daftar topik pertanyaan dan menambah contoh pertanyaan untuk halaman 22–28 | ☐ | Enam pertanyaan halaman 22–28 sudah dipakai dalam percobaan, pemeriksaan label dibawa ke Sprint 5 |
| Mencatat waktu jawab pada setiap uji antarmuka | ☑ | Waktu jawab dicatat pada setiap uji langsung dan percobaan |

## Checklist akhir Sprint

| Butir | Status |
|---|---|
| *Sprint Planning* terlaksana dan divalidasi *Product Owner* | ☑ |
| Logbook diisi setiap hari kerja aktif | ☑ |
| *Sprint Review* terlaksana dan Increment divalidasi *Product Owner* | ☑ |
| *Sprint Retrospective* terlaksana | ☑ |
| Product Backlog diperbarui | ☑ |

## Konfirmasi Scrum Master

Berdasarkan checklist di atas, peristiwa Scrum pada Sprint 4 telah terlaksana sesuai rencana.

| | |
|---|---|
| Jakarta, 19 November 2026<br>Scrum Master,<br><br><br><br>Dr. Widodo, M. Kom.<br>NIP. {{NIP_SCRUM_MASTER_RETRO}} | <br>Developer,<br><br><br><br>Deni Merdiansyah<br>NIM {{NIM_DEVELOPER}} |

*Dasar penyusunan: Schwaber & Sutherland (2020) untuk komponen Sprint Retrospective. Rujukan lengkap tercantum pada laporan.*
