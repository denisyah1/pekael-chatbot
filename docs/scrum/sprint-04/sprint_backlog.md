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
| S4-T04 | 4 | PBI-06, PBI-07 | Evaluasi dan perbaikan tampilan pertama | In Progress | Evaluasi pertama Developer: tampilan dirancang ulang (tema gelap, intro, informasi umum, tanda proses), menunggu evaluasi kedua |
| S4-T05 | 5 | PBI-08 | Login satu akun admin | To Do | |
| S4-T06 | 6 | PBI-08 | Halaman admin untuk mengganti buku panduan dan laporan pembangunan | To Do | |
| S4-T07 | 7 | PBI-06 | Pembatasan panjang pertanyaan dan pencegahan pengiriman berulang | In Progress | Batas 500 karakter aktif. Kolom pertanyaan terkunci selama jawaban disusun, sehingga pertanyaan tidak terkirim berulang |
| S4-T08 | 8 | PBI-06, PBI-07, PBI-08 | Pengujian otomatis tampilan dan uji seluruh penggunaan dari website | In Progress | 12 pengujian otomatis halaman mahasiswa lulus |

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

### 14 November 2026

**Dikerjakan**
- Developer mengevaluasi tampilan pertama dan menilainya terlalu polos. Permintaan perbaikan: huruf modern yang santai, warna gelap perpaduan navy dan abu kebiruan, perkenalan (intro) yang membuat mahasiswa penasaran dan nyaman sebelum bertanya, nama Pekael dengan tipografi yang khas, tanda proses pada setiap tahap, dan informasi umum agar halaman tidak kosong.
- Merancang ulang tampilan dengan konsep "PKL, kalau dibaca jadi pe·ka·el":
  - intro diawali tiga huruf p, k, l yang berjauhan, lalu huruf e, a, e tumbuh di antaranya dengan huruf miring yang lebih lembut sehingga terbaca "pekael", disusul garis seperti coretan tangan, dua kalimat perkenalan, fakta PKL yang berganti, dan tombol "Mulai bertanya",
  - latar navy dengan garis halus seperti kertas buku dan nomor halaman yang melayang pelan, karena setiap jawaban Pekael menyebut halaman buku pedoman,
  - huruf utama Plus Jakarta Sans, huruf aksen Fraunces miring, warna navy dan abu kebiruan dengan aksen biru muda dan krem,
  - halaman tanya-jawab berisi sapaan, empat contoh pertanyaan yang dapat langsung diklik, dan enam fakta singkat PKL beserta halamannya,
  - pertanyaan tampil sebagai gelembung di kanan, jawaban dalam kartu berlabel "Dari buku pedoman" dengan penanda halaman dan kutipan,
  - panel samping berisi cara kerja Pekael, sumber jawaban, tombol percakapan baru, dan tombol memutar ulang intro.
- Menambahkan tanda proses pada setiap tahap: "Menyiapkan buku pedoman" saat halaman pertama dibuka, lalu saat menjawab tulisan berganti sesuai langkah yang benar-benar sedang berjalan (membaca pertanyaan, membuka buku pedoman, memilih halaman, mengumpulkan kutipan, menyusun jawaban, mencocokkan halaman), disertai satu fakta PKL sambil menunggu.
- Kolom pertanyaan dikunci selama jawaban disusun agar pertanyaan tidak terkirim berulang.
- Mengganti pesan gangguan yang memakai istilah "AI" dengan bahasa yang lebih wajar.
- Memastikan seluruh fakta yang ditampilkan sesuai dengan teks buku pedoman yang sudah diverifikasi.

**Hasil uji**
- Pengujian otomatis: 237 lulus, 0 gagal, termasuk 12 pengujian halaman mahasiswa dan 1 pengujian tanda proses.
- Tampilan diperiksa melalui tangkapan layar pada ukuran laptop dan ponsel: intro, layar persiapan, halaman awal, tanda proses, dan jawaban dengan pertanyaan "nilai 74, lulus atau tidak" (rujukan halaman 11 dan 16).

**Hambatan**
- Tidak ada.

**Berikutnya**
- Evaluasi kedua tampilan oleh Developer (S4-T04).
- Pemeriksaan ulang label halaman daftar topik (S4-T01).

### 15 November 2026

**Dikerjakan**
- Developer menemukan pertanyaan yang gagal dijawab setelah menunggu 62 detik dengan pesan layanan sedang sibuk.
- Menelusuri penyebabnya dengan memanggil Gemini secara langsung. Model `gemini-3.5-flash-lite` sedang sangat lambat: pertanyaan satu kata memerlukan 10–44 detik dan satu kali ditolak server karena melewati batas waktu. Pada Sprint 3 pertanyaan yang sama memerlukan 1–2 detik. Model `gemini-3.5-flash` pada saat yang sama memerlukan 3–5 detik.
- Waktu 62 detik berasal dari dua kali menunggu 30 detik: permintaan yang habis waktunya dicoba ulang. Percobaan ulang kini hanya dilakukan bila server sibuk, tidak untuk permintaan yang sudah menunggu sampai batas waktu, sehingga mahasiswa paling lama menunggu satu kali batas waktu.
- Batas waktu menunggu Gemini dapat diatur dari pengaturan (bawaan 30 detik).
- Tanda proses pada tahap menyusun jawaban kini memberi tahu bahwa tahap tersebut kadang lebih lama saat layanan ramai.

**Hasil uji**
- Pengujian otomatis: 240 lulus, 0 gagal, termasuk pengujian bahwa permintaan yang habis waktunya tidak dicoba ulang.

- Atas keputusan Developer, model `gemini-3.5-flash` dicoba dengan 44 pertanyaan yang sama seperti EXP-004 (EXP-005). Setelah sekitar 15 pertanyaan, semua permintaan ditolak karena kuota gratis model tersebut hanya 20 permintaan per hari. Pertanyaan yang sempat dijawab pun memerlukan 4–28 detik.
- Model dikembalikan ke `gemini-3.5-flash-lite`.

**Hambatan**
- Kecepatan layanan Gemini gratis berubah-ubah dan berada di luar kendali Pekael. Kuota harian `gemini-3.5-flash-lite` perlu dicek Developer di Google AI Studio sebelum UAT.

**Berikutnya**
- Evaluasi kedua tampilan oleh Developer (S4-T04).
