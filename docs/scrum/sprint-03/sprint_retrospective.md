# Lembar Validasi Sprint Report 3 — Bagian C: Sprint Retrospective

| | |
|---|---|
| Sprint | : Sprint 3 |
| Periode Sprint | : 6 – 12 November 2026 |
| Tanggal *Sprint Retrospective* | : 12 November 2026 |
| Scrum Master | : Dosen pembimbing |
| Developer | : Deni Merdiansyah (NIM {{NIM_DEVELOPER}}) |

## Tujuan

Lembar ini memuat hasil *Sprint Retrospective* Sprint 3, yaitu evaluasi cara kerja selama sprint dan rencana perbaikan untuk sprint berikutnya, untuk dikonfirmasi oleh Scrum Master.

## Yang berjalan baik

- Seluruh tugas pengembangan selesai pada 8 November 2026, lebih awal dari rencana 12 November, sehingga tersisa waktu untuk pemeriksaan jawaban dan pengujian tambahan.
- Pengujian otomatis menemukan kesalahan sebelum dipakai: pesan "knowledge base belum disiapkan" sempat tertimpa pesan penolakan dan langsung diperbaiki.
- Uji langsung menemukan perilaku Gemini yang perlu ditangani, yaitu salam pembuka pada jawaban dan pengaturan keseragaman jawaban yang diabaikan model.
- Aturan penentuan batas kedekatan ditetapkan sebelum percobaan dijalankan, sehingga nilai batas tidak disesuaikan dengan hasil yang diinginkan.
- Kondisi gagal diuji dua cara, langsung dan dengan tiruan layanan, sehingga kondisi yang sulit dipicu (kuota habis, layanan sibuk) tetap teruji tanpa menghabiskan kuota.
- Waktu jawab ternyata lebih baik dari perkiraan awal Sprint 3, dengan nilai tengah sekitar 1,7 detik.

## Yang perlu diperbaiki

- Verifikasi koreksi OCR halaman tambahan baru selesai menjelang *Sprint Review*, setelah seluruh tugas lain selesai. Pemeriksaan oleh Developer perlu dijadwalkan pada hari pertama sprint.
- Pertanyaan contoh untuk halaman 22–28 baru berjumlah 6. Halaman tersebut perlu lebih banyak contoh pertanyaan pada dataset evaluasi.
- Pemeriksaan ulang label halaman pada daftar topik pertanyaan (rencana perbaikan Sprint 2) belum dilakukan bersama Developer.

## Hambatan dan penyebab

| Hambatan | Penyebab | Dampak pada sprint |
|---|---|---|
| Waktu jawab kadang lebih dari 5 detik (paling lama 13 detik) | Kondisi server Gemini pada layanan gratis | Belum memengaruhi fungsi, dipantau pada Sprint 4 dan 5 |
| Jawaban dapat sedikit berbeda setiap kali ditanya | Model Gemini yang dipakai memakai pengaturan tetap dan mengabaikan pengaturan keseragaman | Perlu dicatat pada evaluasi agar hasil dapat ditelusuri |
| Satu pertanyaan dalam cakupan ditolak dan satu jawaban kurang lengkap | Potongan yang relevan berada di peringkat bawah atau tidak terambil | Bahan uji ulang pengaturan pada Sprint 5 |

## Rencana perbaikan untuk Sprint 4

| Tindakan | Penanggung jawab | Diperiksa pada |
|---|---|---|
| Menjadwalkan pemeriksaan hasil kerja yang memerlukan Developer atau *Product Owner* pada hari pertama sprint | Developer | *Sprint Review* Sprint 4 |
| Memeriksa ulang label halaman pada daftar topik pertanyaan dan menambah contoh pertanyaan untuk halaman 22–28 | Developer | *Sprint Review* Sprint 4 |
| Mencatat waktu jawab pada setiap uji antarmuka | Developer | *Sprint Review* Sprint 4 |

## Tindak lanjut rencana perbaikan Sprint 2

| Tindakan | Terlaksana | Catatan |
|---|---|---|
| Menetapkan jadwal tetap pertemuan dengan *Product Owner* di awal sprint | ☑ | Pemeriksaan contoh jawaban dijadwalkan pada *Sprint Planning* (10 November 2026) |
| Memeriksa ulang label halaman pada daftar topik pertanyaan bersama Developer | ☐ | Belum dilakukan, dibawa ke rencana perbaikan Sprint 4 |
| Mengajukan usulan perubahan ruang lingkup hanya pada *Sprint Planning* atau *Sprint Review* | ☑ | Tidak ada perubahan ruang lingkup selama Sprint 3 |

## Checklist akhir Sprint

| Butir | Status |
|---|---|
| *Sprint Planning* terlaksana dan divalidasi *Product Owner* | ☑ |
| Logbook diisi setiap hari kerja aktif | ☑ |
| *Sprint Review* terlaksana dan Increment divalidasi *Product Owner* | ☑ |
| *Sprint Retrospective* terlaksana | ☑ |
| Product Backlog diperbarui | ☑ |

## Konfirmasi Scrum Master

Berdasarkan checklist di atas, peristiwa Scrum pada Sprint 3 telah terlaksana sesuai rencana.

| | |
|---|---|
| Jakarta, 12 November 2026<br>Scrum Master,<br><br><br><br>Dr. Widodo, M. Kom. | <br>Developer,<br><br><br><br>Deni Merdiansyah<br>NIM {{NIM_DEVELOPER}} |

*Dasar penyusunan: Schwaber & Sutherland (2020) untuk komponen Sprint Retrospective. Rujukan lengkap tercantum pada laporan.*
