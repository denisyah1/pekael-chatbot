# Sprint Backlog — Sprint 3

> **Sprint Goal:** Menghasilkan alur tanya-jawab Pekael yang berjalan lengkap tanpa antarmuka: knowledge base tersimpan di FAISS dan dapat dimuat ulang, pertanyaan dicarikan potongan teks yang relevan, Gemini menyusun jawaban hanya dari potongan tersebut beserta rujukan halaman, dan pertanyaan di luar cakupan dijawab dengan pesan penolakan, sebagai dasar antarmuka Streamlit pada Sprint 4.
> **Periode:** 6 – 12 November 2026
> **Status task:** `To Do` · `In Progress` · `Done` · `Blocked`
> **Rincian teknis:** [`docs/technical/sprint-03.md`](../../technical/sprint-03.md)

## Task

Sprint Planning memuat tujuh tugas (lihat [Sprint Planning](sprint_planning.md) bagian 4). Kolom **Tugas** menunjukkan nomor tugas pada Sprint Planning.

| ID | Tugas | PBI | Pekerjaan | Status | Bukti |
|---|---|---|---|---|---|
| S3-T01 | 1 | PBI-01 | Pemeriksaan dan koreksi OCR halaman 22–25 dan 27–28, termasuk penulisan ulang tabel halaman 27–28 (bawaan S2-T10) | To Do | |
| S3-T02 | 1 | PBI-01 | Mengganti pengaturan halaman knowledge base menjadi 4–16, 22–25, 27–28 setelah S3-T01 selesai | To Do | |
| S3-T03 | 2 | PBI-04 | Penyimpanan FAISS: membangun, menyimpan berversi, memuat ulang, dan mempertahankan indeks lama bila pembangunan gagal | Done | Pengujian otomatis 13 skenario lulus |
| S3-T04 | 3 | PBI-05 | Penghubung model Gemini untuk menyusun jawaban dan penanganan gangguan layanan | To Do | |
| S3-T05 | 4 | PBI-05 | Instruksi (prompt) untuk Gemini: menjawab hanya dari konteks, menyatakan bila informasi tidak ditemukan | To Do | |
| S3-T06 | 4 | PBI-05 | Alur tanya-jawab berurutan beserta pemeriksaan rujukan | To Do | |
| S3-T07 | 5 | PBI-04, PBI-05 | Perakitan komponen dan perintah terminal untuk membangun knowledge base dan bertanya | To Do | |
| S3-T08 | 6 | PBI-05 | Kalibrasi awal batas relevansi (EXP-003) | To Do | |
| S3-T09 | 7 | PBI-05 | Uji kondisi gagal | To Do | |

## Log Pengerjaan

### 6 November 2026

**Dikerjakan**
- Menyusun *Sprint Planning* Sprint 3 (Lembar Validasi Bagian A).
- Membawa pekerjaan Sprint 2 yang belum selesai, yaitu pemeriksaan OCR halaman 22–25 dan 27–28, ke Sprint 3 sebagai tugas pertama.
- Membuat penyimpanan knowledge base di FAISS. Setiap kali knowledge base dibangun, hasilnya disimpan sebagai versi baru di folder tersendiri lengkap dengan catatan pembangunannya (model, ukuran vektor, jumlah potongan, halaman, dan sidik dokumen). Versi baru hanya dipakai setelah berhasil dimuat ulang dan diperiksa. Bila pembangunan gagal, versi lama tetap dipakai. Dua versi terakhir disimpan untuk cadangan.
- Memastikan knowledge base tidak dipakai bila dibangun dengan model embedding yang berbeda dari pengaturan, agar hasil pencarian tidak keliru.

**Hasil uji**
- Pengujian otomatis: 156 lulus, 0 gagal. Pengujian baru mencakup pembangunan, pemuatan ulang seolah aplikasi dijalankan ulang, pencarian, penggantian versi, pembersihan versi lama, pembangunan yang gagal, dan knowledge base yang belum dibangun.

**Hambatan**
- Tidak ada.

**Berikutnya**
- Pemeriksaan OCR halaman 22–25 dan 27–28 (S3-T01).
- Penghubung model Gemini dan instruksi jawaban (S3-T04, S3-T05).
