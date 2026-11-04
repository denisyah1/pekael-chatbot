# Sprint Backlog — Sprint 4

> **Sprint Goal:** Menghasilkan website Pekael yang dapat dipakai secara lokal: mahasiswa dapat mengetik pertanyaan dan menerima jawaban beserta rujukan halaman buku panduan melalui tampilan yang sederhana dan mudah dipahami, admin dapat masuk dengan satu akun lalu memperbarui buku panduan tanpa menghilangkan knowledge base yang sedang dipakai, dan seluruh fungsi diuji sebelum validasi ahli pada Sprint 5.
> **Periode:** 13 – 26 November 2026
> **Status task:** `To Do` · `In Progress` · `Done` · `Blocked`
> **Rincian teknis:** [`docs/technical/sprint-04.md`](../../technical/sprint-04.md)

## Task

Sprint Planning memuat delapan tugas (lihat [Sprint Planning](sprint_planning.md) bagian 4). Kolom **Tugas** menunjukkan nomor tugas pada Sprint Planning.

| ID | Tugas | PBI | Pekerjaan | Status | Bukti |
|---|---|---|---|---|---|
| S4-T01 | 1 | PBI-06 | Pemeriksaan ulang label halaman daftar topik dan penambahan contoh pertanyaan halaman 22–28 | To Do | |
| S4-T02 | 2 | PBI-06 | Halaman tanya-jawab mahasiswa | In Progress | Tampilan pertama selesai, menunggu evaluasi Developer |
| S4-T03 | 3 | PBI-07 | Rujukan dokumen, halaman PDF, bagian, dan kutipan | In Progress | Tampil pada setiap jawaban, menunggu evaluasi Developer |
| S4-T04 | 4 | PBI-06, PBI-07 | Evaluasi dan perbaikan tampilan pertama | To Do | |
| S4-T05 | 5 | PBI-08 | Login satu akun admin | To Do | |
| S4-T06 | 6 | PBI-08 | Halaman admin untuk mengganti buku panduan dan laporan pembangunan | To Do | |
| S4-T07 | 7 | PBI-06 | Pembatasan panjang pertanyaan dan pencegahan pengiriman berulang | In Progress | Batas 500 karakter aktif pada kolom pertanyaan, pencegahan pengiriman berulang belum |
| S4-T08 | 8 | PBI-06, PBI-07, PBI-08 | Pengujian otomatis tampilan dan uji seluruh penggunaan dari website | In Progress | 9 pengujian otomatis halaman mahasiswa lulus |

## Log Pengerjaan

### 13 November 2026

**Dikerjakan**
- Menyusun *Sprint Planning* Sprint 4 (Lembar Validasi Bagian A).
- Membuat tampilan pertama halaman tanya-jawab mahasiswa dengan prinsip sederhana dan wajar untuk layanan akademik:
  - judul Pekael dan satu kalimat penjelasan layanan, tanpa istilah "AI", "asisten virtual", atau ikon robot,
  - satu kolom pertanyaan dengan contoh pertanyaan dan tombol Kirim,
  - tulisan "Mencari jawaban di buku pedoman..." selama jawaban disusun,
  - jawaban terbaru tampil paling atas dalam kotak, disertai baris sumber (nama dokumen dan halaman PDF) dan bagian "Lihat kutipan dari buku pedoman",
  - pesan penolakan ditampilkan dengan warna netral, gangguan layanan dengan warna peringatan,
  - tombol "Hapus riwayat" dan catatan bahwa keputusan resmi tetap mengikuti buku pedoman atau koordinator PKL.
- Bila pengaturan belum lengkap atau knowledge base belum dimuat, kolom pertanyaan dinonaktifkan dan pesan yang jelas ditampilkan.
- Riwayat tanya-jawab hanya tampil selama halaman dibuka dan tidak dikirim ke Gemini, sesuai ketentuan tanpa memory.
- Warna tampilan memakai satu warna hijau sebagai aksen di atas latar putih.
- Menambahkan cara menjalankan website secara lokal pada README.

**Hasil uji**
- Pengujian otomatis: 233 lulus, 0 gagal, termasuk 9 pengujian baru untuk halaman mahasiswa.
- Website menyala secara lokal dan dapat dibuka.
- Uji halaman dengan knowledge base dan Gemini yang sebenarnya: pertanyaan "nilai 74, lulus atau tidak" dijawab dengan sumber halaman PDF 11 dan 16. Pertanyaan di luar topik PKL ditolak dalam 0,5 detik.
- Pertanyaan pertama setelah website dinyalakan memerlukan 19,7 detik.

**Hambatan**
- Waktu jawab pertanyaan pertama setelah website dinyalakan jauh lebih lama daripada pertanyaan berikutnya. Diukur ulang pada uji waktu jawab (S4-T08).

**Berikutnya**
- Developer mengevaluasi tampilan pertama (S4-T04).
- Pemeriksaan ulang label halaman daftar topik (S4-T01).
