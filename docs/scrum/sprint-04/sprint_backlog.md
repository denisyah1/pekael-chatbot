# Sprint Backlog — Sprint 4

> **Sprint Goal:** Menghasilkan website Pekael yang dapat dipakai secara lokal: mahasiswa dapat mengetik pertanyaan dan menerima jawaban beserta rujukan halaman buku panduan melalui tampilan yang sederhana dan mudah dipahami, admin dapat masuk dengan satu akun lalu memperbarui buku panduan tanpa menghilangkan knowledge base yang sedang dipakai, dan seluruh fungsi diuji sebelum validasi ahli pada Sprint 5.
> **Periode:** 13 – 19 November 2026
> **Status task:** `To Do` · `In Progress` · `Done` · `Blocked`
> **Rincian teknis:** [`docs/technical/sprint-04.md`](../../technical/sprint-04.md)

## Task

Sprint Planning memuat sembilan tugas (lihat [Sprint Planning](sprint_planning.md) bagian 4). Kolom **Tugas** menunjukkan nomor tugas pada Sprint Planning.

| ID | Tugas | PBI | Pekerjaan | Status | Bukti |
|---|---|---|---|---|---|
| S4-T01 | 1 | PBI-06 | Pemeriksaan ulang label halaman daftar topik dan penambahan contoh pertanyaan halaman 22–28 | Dibawa ke Sprint 5 | Enam pertanyaan halaman 22–28 dipakai pada percobaan, pemeriksaan label dibawa ke Sprint 5 |
| S4-T02 | 2 | PBI-06 | Halaman tanya-jawab mahasiswa | Done | Intro, halaman tanya-jawab, contoh pertanyaan, fakta PKL, gaya jawaban adaptif dan bervariasi |
| S4-T03 | 3 | PBI-07 | Rujukan dokumen, halaman PDF, bagian, dan kutipan | Done | Nama dokumen, penanda halaman PDF, dan kutipan pada setiap jawaban |
| S4-T04 | 4 | PBI-06, PBI-07 | Evaluasi dan perbaikan tampilan pertama | Done | Empat putaran evaluasi Developer dan masukan bimbingan diterapkan |
| S4-T05 | 5 | PBI-08 | Login satu akun admin | Done | Satu akun dari pengaturan lokal, salah kata sandi lima kali mengunci formulir 30 detik |
| S4-T06 | 6 | PBI-08 | Halaman admin untuk mengganti buku panduan dan laporan pembangunan | Done | Ganti dan bangun ulang buku dengan laporan, riwayat versi, uji pertanyaan, 16 pengujian ruang admin lulus |
| S4-T07 | 7 | PBI-06 | Pembatasan panjang pertanyaan dan pencegahan pengiriman berulang | Done | Batas 500 karakter, kolom pertanyaan terkunci selama jawaban disusun, pertanyaan yang sama dijawab dari simpanan |
| S4-T09 | 9 | PBI-06 | Respons arahan untuk pertanyaan yang jawabannya tidak ada di buku pedoman (permintaan *Product Owner*) | Done | Uji langsung 5 pertanyaan PKL yang jawabannya tidak ada di buku dan 3 pertanyaan di luar topik PKL, menunggu tinjauan *Product Owner* |
| S4-T08 | 8 | PBI-06, PBI-07, PBI-08 | Pengujian otomatis tampilan dan uji seluruh penggunaan dari website | Done | 327 pengujian otomatis lulus, uji 44 pertanyaan (EXP-009), tangkapan layar laptop dan ponsel |

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

### 16 November 2026

**Dikerjakan**
- Developer menanyakan apakah knowledge base dibangun ulang setiap website dijalankan. Knowledge base hanya dibangun sekali lalu dimuat dari penyimpanan dalam 0,05 detik. Waktu tunggu jawaban seluruhnya berasal dari Gemini.
- Developer menetapkan tetap memakai `gemini-3.5-flash-lite` dan meminta efisiensi. Ditambahkan simpanan jawaban: pertanyaan yang sama persis (huruf besar-kecil, spasi, dan tanda tanya diabaikan) dijawab dari simpanan tanpa memanggil Gemini. Simpanan hanya berisi pasangan pertanyaan dan jawaban per versi knowledge base, bukan riwayat percakapan, dan dikosongkan saat knowledge base diganti. Jawaban gagal tidak disimpan.
- Evaluasi kedua tampilan oleh Developer: pertanyaan tampil di kanan dan jawaban di kiri seperti aplikasi percakapan, masing-masing dengan jam.
- Membuat ruang admin di alamat `/admin` dengan konsep kartu perpustakaan:
  - halaman masuk berbentuk kartu pengelola dengan punggung buku, garis kertas, dan stempel "RUANG ADMIN",
  - ringkasan buku aktif, jumlah halaman, potongan, dan versi,
  - peta halaman buku: setiap halaman PDF tampil sebagai satu ubin, makin terang makin banyak potongan, halaman yang tidak dipakai bergaris putus-putus,
  - mengganti buku pedoman dengan unggahan PDF (maksimal 30 MB, wajib dicentang sudah disetujui *Product Owner*) atau membangun ulang buku yang sedang dipakai, lengkap dengan tanda proses per halaman dan laporan hasil,
  - riwayat versi dengan tombol untuk mengaktifkan kembali versi sebelumnya,
  - uji pertanyaan lengkap dengan jarak potongan dan batas relevansi,
  - ringkasan pengaturan tanpa menampilkan kata sandi dan API key.
- Developer meminta nama pengguna dan kata sandi admin ditulis langsung di kode. Karena repository bersifat publik, kata sandi di kode dapat dibaca siapa pun. Akun yang diminta tetap dipakai, tetapi disimpan di pengaturan lokal yang tidak ikut ke repository.

**Hasil uji**
- Pengujian otomatis: 274 lulus, 0 gagal, termasuk 14 pengujian simpanan jawaban, kemajuan pembangunan, dan riwayat versi, serta 14 pengujian ruang admin.
- Uji dari website: pertanyaan "Berapa lama PKL dilaksanakan?" pertama kali dijawab dalam 6,1 detik, saat ditanyakan ulang dijawab dalam 1,0 detik dari simpanan. Pertanyaan di luar topik PKL ditolak dalam 2,0 detik.
- Tangkapan layar ukuran laptop dan ponsel: percakapan, halaman masuk admin, ringkasan dan peta halaman, riwayat versi, dan pengaturan.

- Developer mencoba masuk ruang admin dan ditolak. Pengaturan akun terbaca benar dan akun yang diminta lolos pemeriksaan, sehingga penolakan berasal dari teks yang dimasukkan. Agar spasi yang ikut tersalin dan huruf besar pada nama pengguna tidak menggagalkan login, spasi di awal dan akhir kini diabaikan dan nama pengguna tidak membedakan huruf besar-kecil. Kata sandi tetap harus sama persis.
- Developer masih ditolak. Login diuji ulang dengan pengaturan asli dan dengan mengetik langsung di browser, keduanya berhasil masuk. Dugaan penyebab adalah isian otomatis browser yang tampil di layar tetapi tidak terkirim. Isian otomatis kini dimatikan, dan bila kolom terkirim kosong muncul pesan untuk mengetik ulang secara manual tanpa dihitung sebagai percobaan gagal.
- Developer masih ditolak. Ditambahkan perintah pemeriksa login yang dijalankan di terminal Developer untuk menunjukkan asal pengaturan akun dan bagian yang tidak cocok, tanpa menampilkan kata sandi.

**Hambatan**
- Tidak ada.

**Berikutnya**
- Evaluasi tampilan percakapan dan ruang admin oleh Developer.
- Uji mengganti buku pedoman dari website (S4-T06).
- Pemeriksaan ulang label halaman daftar topik (S4-T01).

### 17 November 2026

**Dikerjakan**
- Mencatat keputusan pemilik: Sprint 4 sampai Sprint 6 masing-masing menjadi 1 minggu (Sprint 4 13–19 November, Sprint 5 20–26 November, Sprint 6 27 November–3 Desember 2026). *Sprint Planning* Sprint 4 disesuaikan dengan periode baru.
- Menindaklanjuti masukan bimbingan *Product Owner*: pertanyaan yang jawabannya tidak ada di buku pedoman tidak lagi dijawab dengan kalimat penolakan yang sama setiap kali. Pekael kini menulis 2–3 kalimat yang ramah sesuai topik pertanyaan dan mengarahkan mahasiswa ke pihak yang tepat: Koordinator PKL, Admin Prodi PTIK, atau Koordinator Program Studi (Kaprodi). Pekael tetap tidak menebak jawabannya dan tidak menyebut tanggal, nama, atau nomor kontak yang tidak ada di buku. Bila ada informasi terkait di buku, halamannya ikut ditampilkan.
- Pertanyaan di luar topik PKL dijawab dengan salah satu dari beberapa kalimat ajakan kembali ke topik PKL, tanpa memanggil Gemini.
- Ungkapan seperti "tidak dapat dijawab", "tidak ditemukan", "tidak tersedia", "di luar cakupan", dan "knowledge base" dicegah. Bila Gemini tetap memakainya, kalimat diganti dengan arahan siap pakai.
- Label jawaban arahan di halaman mahasiswa diganti dari "Tidak ada di buku pedoman" menjadi "Saran dari Pekael".

**Hasil uji**
- Pengujian otomatis: 296 lulus, 0 gagal.
- Uji langsung pertama: arahan sudah ramah, tetapi dua jawaban masih memakai "tidak tersedia" dan "belum tercantum", sebagian menyalin daftar tugas pihak yang dituju, dan sapaan bercampur "Anda" dan "kamu". Instruksi diperketat.
- Uji langsung kedua: lima pertanyaan PKL yang jawabannya tidak ada di buku dijawab dengan arahan yang berbeda-beda tanpa kalimat penolakan, misalnya batas pendaftaran diarahkan ke Admin Prodi PTIK dan kerja paruh waktu selama PKL ke Koordinator PKL. Jawaban untuk pertanyaan yang ada di buku tidak berubah.

**Hambatan**
- Tidak ada.

**Berikutnya**
- *Product Owner* meninjau contoh respons arahan.
- Menyiapkan penambahan knowledge base dari *Product Owner* setelah bimbingan.
- Pemeriksaan ulang label halaman daftar topik (S4-T01), uji mengganti buku dari website (S4-T06), dan pengujian seluruh penggunaan (S4-T08).

### 18 November 2026

**Dikerjakan**
- Menindaklanjuti masukan dosen pembimbing: jawaban Pekael dinilai masih kaku dan seragam. Pekael kini menyesuaikan gaya bahasa dengan cara mahasiswa bertanya. Pertanyaan santai dijawab santai dengan sapaan "kamu", pertanyaan formal dijawab dengan bahasa baku dan sapaan "Anda". Isi buku dijelaskan dengan kalimat sendiri, sedangkan angka, nilai, nama dokumen, dan isi daftar syarat tetap persis.
- Gaya pertanyaan dikenali dari kata-kata yang dipakai (misalnya "kak", "gak", "sih" untuk santai, "mohon", "apakah", "mengenai" untuk formal), karena Gemini belum konsisten mengenalinya sendiri.
- Sapaan, ucapan terima kasih, dan curhat kini dibalas seperti percakapan biasa, tanpa memberi informasi PKL yang tidak bersumber.
- Uji langsung menemukan kesalahan serius: pertanyaan santai "kalo nilai aku 74 lulus gak?" dijawab "lulus". Penyebabnya, potongan buku yang memuat syarat kelulusan B+ ikut terbuang oleh batas kedekatan. Kini batas kedekatan hanya menentukan pertanyaan diterima atau ditolak, dan semua potongan yang ditemukan tetap dipakai. Instruksi juga diperketat: sebelum menyimpulkan lulus atau memenuhi syarat, syarat yang menentukan harus dicari dan disebutkan.
- Memperbaiki waktu persiapan. Bagian yang hanya dibutuhkan saat membangun knowledge base (pembaca PDF dan OCR) tidak lagi dimuat saat Pekael dijalankan. Saat intro tampil, Pekael menyiapkan diri di belakang layar, termasuk membuka koneksi pertama ke layanan Gemini, sehingga halaman tanya-jawab dan jawaban pertama tidak menunggu lama.

**Hasil uji**
- Pengujian otomatis: 315 lulus, 0 gagal.
- Waktu persiapan sebelum pertanyaan pertama dapat dijawab: sekitar 20 detik sebelum perbaikan, sekitar 7 detik sesudahnya, dan di website berlangsung selama intro.
- Uji 44 pertanyaan dengan gaya bahasa baru (EXP-007): 36 dari 36 pertanyaan dalam cakupan dijawab, termasuk satu pertanyaan yang sebelumnya ditolak. Lima pertanyaan PKL yang jawabannya tidak ada di buku diarahkan ke pihak yang tepat, tiga pertanyaan di luar topik PKL dibalas seperti percakapan. Tidak ada ungkapan penolakan. Waktu jawab umumnya 2,8 detik.
- Pasangan pertanyaan santai dan formal untuk topik yang sama dijawab dengan isi yang sama dan gaya yang berbeda.

**Hambatan**
- Balasan percakapan untuk pesan di luar topik PKL sempat memerlukan sekitar 8 detik pada uji ini. Dipantau pada uji berikutnya.

**Berikutnya**
- Developer mencoba gaya jawaban baru dan waktu masuk dari intro di website.
- Rancangan pengelolaan knowledge base di ruang admin untuk dokumen tambahan dari *Product Owner*.
- *Sprint Review* dan *Retrospective* Sprint 4 (19 November).

### 19 November 2026

**Dikerjakan**
- Menindaklanjuti evaluasi Developer: jawaban untuk pertanyaan dengan maksud yang sama, misalnya "apa itu PKL", masih disajikan dengan bentuk yang sama. Kini setiap jawaban memakai satu bentuk penyajian yang dipilih acak, misalnya langsung ke inti, beberapa poin pendek, atau penjelasan sederhana seperti ke teman. Isi dan daftar syarat tetap sama. Arahan ke Koordinator PKL, Admin Prodi PTIK, atau Koordinator Program Studi (Kaprodi) juga disampaikan dengan beberapa bentuk, dan jawaban diminta lebih ringkas.
- Kalimat siap pakai cadangan ditambah menjadi enam untuk arahan dan enam untuk pesan di luar topik PKL.
- Menelusuri waktu jawab yang terasa lebih lama. Instruksi lama dan instruksi baru dibandingkan pada pertanyaan dan waktu yang sama, demikian juga pengaturan tingkat berpikir Gemini. Perbedaannya kecil, sehingga lamanya waktu jawab berasal dari kondisi layanan Gemini.
- Developer melaporkan beberapa pertanyaan tidak terjawab setelah perubahan bentuk penyajian. Penyebabnya, petunjuk bentuk arahan yang disertakan di setiap pertanyaan membuat Gemini mengarahkan pertanyaan yang sebenarnya ada jawabannya, misalnya dokumen lampiran laporan. Petunjuk itu dipindahkan ke akhir instruksi utama. Penanda khusus yang salah ditulis Gemini kini tetap dikenali walaupun menyatu dengan teks, dan sapaan pembuka yang tidak diminta dibuang.
- Menyesuaikan format tanda tangan untuk Sprint 4 sampai 6 sesuai lampiran laporan: *Sprint Planning* oleh *Product Owner*, *Sprint Review* oleh Scrum Master Nur Elah, *Sprint Retrospective* oleh Scrum Master Dr. Widodo.
- Menyusun *Sprint Review* dan *Sprint Retrospective* Sprint 4.
- Menyusun [daftar 36 pertanyaan uji](pertanyaan_uji.md) beserta halaman sumber dan hasil uji terakhir, sebagai lampiran.

**Hasil uji**
- Pengujian otomatis: 327 lulus, 0 gagal.
- Perbandingan waktu (EXP-008): instruksi lama median 7,2 detik, instruksi baru 7,0 detik. Tingkat berpikir bawaan 8,0 detik, minimal 8,7 detik. Pada uji 44 pertanyaan sehari sebelumnya, instruksi yang sama memerlukan median 2,8 detik.
- Uji langsung delapan pertanyaan: tiga pertanyaan "apa itu PKL" dengan gaya berbeda dijawab dengan isi yang sama dan penyajian berbeda. Tiga pertanyaan yang jawabannya tidak ada di buku diarahkan dengan cara berbeda.
- Uji ulang 44 pertanyaan setelah perbaikan (EXP-009): 35 dari 36 pertanyaan dalam cakupan dijawab, termasuk dokumen lampiran dan nilai 74 yang dijawab dengan benar. Satu pertanyaan tentang pembekalan diarahkan ke Admin Prodi PTIK. Waktu jawab median 5,4 detik.

**Hambatan**
- Kecepatan layanan Gemini versi gratis berubah-ubah sepanjang hari dan berada di luar kendali Pekael.

**Berikutnya**
- *Sprint Planning* Sprint 5 (20 November 2026).
- Pemeriksaan label daftar topik (bawaan S4-T01) dan pengelolaan beberapa dokumen knowledge base.
