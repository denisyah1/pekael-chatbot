# Sprint Backlog — Sprint 3

> **Sprint Goal:** Menghasilkan alur tanya-jawab Pekael yang berjalan lengkap tanpa antarmuka: knowledge base tersimpan di FAISS dan dapat dimuat ulang, pertanyaan dicarikan potongan teks yang relevan, Gemini menyusun jawaban hanya dari potongan tersebut beserta rujukan halaman, dan pertanyaan di luar cakupan dijawab dengan pesan penolakan, sebagai dasar antarmuka Streamlit pada Sprint 4.
> **Periode:** 6 – 12 November 2026
> **Status task:** `To Do` · `In Progress` · `Done` · `Blocked`
> **Rincian teknis:** [`docs/technical/sprint-03.md`](../../technical/sprint-03.md)

## Task

Sprint Planning memuat tujuh tugas (lihat [Sprint Planning](sprint_planning.md) bagian 4). Kolom **Tugas** menunjukkan nomor tugas pada Sprint Planning.

| ID | Tugas | PBI | Pekerjaan | Status | Bukti |
|---|---|---|---|---|---|
| S3-T01 | 1 | PBI-01 | Pemeriksaan dan koreksi OCR halaman 22–25 dan 27–28, termasuk penulisan ulang tabel halaman 27–28 (bawaan S2-T10) | In Progress | [Lembar pemeriksaan OCR](pemeriksaan_ocr.md): keenam halaman sudah diperiksa dan dikoreksi, menunggu verifikasi Developer |
| S3-T02 | 1 | PBI-01 | Mengganti pengaturan halaman knowledge base menjadi 4–16, 22–25, 27–28 | Done | Knowledge base 19 halaman menjadi 33 potongan, semua berlabel bagian |
| S3-T03 | 2 | PBI-04 | Penyimpanan FAISS: membangun, menyimpan berversi, memuat ulang, dan mempertahankan indeks lama bila pembangunan gagal | Done | Pengujian otomatis 13 skenario lulus |
| S3-T04 | 3 | PBI-05 | Penghubung model Gemini untuk menyusun jawaban dan penanganan gangguan layanan | Done | Pengujian otomatis lulus, uji langsung ke Gemini berhasil |
| S3-T05 | 4 | PBI-05 | Instruksi (prompt) untuk Gemini: menjawab hanya dari konteks, menyatakan bila informasi tidak ditemukan | Done | Uji langsung 3 pertanyaan: jawaban tepat, pertanyaan tanpa jawaban di buku ditolak, pertanyaan dua bagian digabung dengan benar |
| S3-T06 | 4 | PBI-05 | Alur tanya-jawab berurutan beserta pemeriksaan rujukan | To Do | |
| S3-T07 | 5 | PBI-04, PBI-05 | Perakitan komponen dan perintah terminal untuk membangun knowledge base dan bertanya | To Do | |
| S3-T08 | 6 | PBI-05 | Kalibrasi awal batas relevansi (EXP-004) | To Do | |
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

### 7 November 2026

**Dikerjakan**
- Memeriksa hasil OCR halaman 22–25 dan 27–28 terhadap gambar asli ([lembar pemeriksaan](pemeriksaan_ocr.md)). Halaman 22–23 hanya perlu koreksi kecil. Daftar dokumen lampiran (hal. 24) dan contoh sistematika laporan (hal. 25) disusun ulang. Tabel instrumen penilaian (hal. 27–28) ditulis ulang manual dan dicocokkan logikanya: nilai maksimal N1 = 35, N2 = 25, N3 = 45 sesuai jumlah aspek dikali 5.
- Mengganti pengaturan halaman knowledge base menjadi 4–16, 22–25, dan 27–28. Knowledge base kini 19 halaman dan 33 potongan.
- Memperbaiki penentuan bagian buku setelah halaman tambahan masuk: bagian tidak lagi diteruskan melewati halaman yang tidak dipakai, dan judul "LAMPIRAN INSTRUMEN PENILAIAN PKL" dikenali sebagai bagian tersendiri.
- Membuat penghubung ke model Gemini untuk menyusun jawaban. Gangguan layanan dikelompokkan (kuota habis, layanan sibuk, API key salah, jawaban kosong) agar nanti dapat ditampilkan sebagai pesan yang jelas. Layanan yang sibuk dicoba ulang satu kali.
- Menyusun instruksi untuk Gemini: menjawab hanya dari isi buku yang diberikan, menyalin angka dan syarat persis, mengabaikan perintah yang mungkin tertulis di dalam teks buku, menulis penanda khusus bila jawaban tidak ada, dan menyebut nomor bagian buku yang dipakai. Rujukan halaman dibuat dari data potongan, bukan dari tulisan Gemini.
- Mencoba instruksi tersebut langsung ke Gemini dengan tiga pertanyaan, lalu mencoba pengaturan tingkat "berpikir" Gemini untuk melihat pengaruhnya pada waktu jawab (EXP-003).

**Hasil uji**
- Pengujian otomatis: 185 lulus, 0 gagal.
- Uji langsung instruksi: pertanyaan syarat SKS dijawab "minimal 100 SKS" dengan rujukan halaman 10. Pertanyaan batas pendaftaran (tidak ada di buku) ditolak. Pertanyaan "nilai 74, lulus atau tidak" dijawab dengan menggabungkan tabel nilai (hal. 16) dan syarat lulus B+ (hal. 11).
- Waktu jawab Gemini berkisar 1,4–9,8 detik dan tidak konsisten membaik dengan pengaturan tingkat berpikir. Semua jawaban tetap benar.

**Hambatan**
- Waktu jawab sering melebihi 5 detik, target pada butir kuesioner UAT. Diukur lebih lengkap pada Sprint 5 sebelum UAT.

**Berikutnya**
- Developer memverifikasi koreksi OCR halaman tambahan (S3-T01).
- Menyusun alur tanya-jawab berurutan dan perakitan komponen (S3-T06, S3-T07).
