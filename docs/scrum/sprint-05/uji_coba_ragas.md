# Laporan Uji Coba Evaluasi Ragas

| | |
|---|---|
| Sprint | : Sprint 5 |
| Tanggal | : 25 November 2026 |
| Data uji | : 36 pertanyaan uji Sprint 4 dari dataset evaluasi versi v2 (belum divalidasi *Product Owner*) |
| Penilai | : Ragas 0.4.3 dengan model penilai `openai/gpt-oss-120b` (layanan Groq versi gratis) dan embedding Gemini |
| Status | : 18 dari 36 pertanyaan selesai dinilai, sisanya menunggu kuota harian Groq |

## Tujuan

Uji coba ini memastikan bahwa evaluasi Ragas dengan tiga metrik penelitian dapat dijalankan dari awal sampai akhir sebelum evaluasi akhir pada Sprint 6. Hasilnya belum menjadi hasil penelitian karena dataset belum divalidasi *Product Owner* dan pengaturan Pekael belum dibekukan.

## Cara kerja evaluasi secara umum

Untuk setiap pertanyaan dilakukan empat langkah:

1. Pekael menjawab pertanyaan seperti saat dipakai mahasiswa. Yang disimpan adalah jawaban Pekael dan empat potongan teks yang ditemukan Pekael dari knowledge base (disebut konteks).
2. Jawaban, konteks, dan jawaban acuan dari dataset diberikan kepada model penilai.
3. Model penilai menjalankan tiga metrik. Setiap metrik menghasilkan nilai 0 sampai 1, makin besar makin baik.
4. Semua langkah perantara, misalnya pernyataan yang dipecah dan alasan penilai, disimpan sehingga setiap nilai dapat diperiksa ulang.

Model penilai berbeda dengan model yang menjawab. Pekael menjawab dengan Gemini, sedangkan penilaian dilakukan oleh model lain (Groq) agar Pekael tidak menilai dirinya sendiri.

## Contoh lengkap: satu pertanyaan

Contoh berikut memakai pertanyaan no. 14 karena jawabannya pendek dan ketiga metriknya menunjukkan hal yang berbeda.

**Pertanyaan:** Apa syarat tambahan kalau PKL di luar negeri?

**Jawaban acuan (dari dataset):** Mahasiswa yang melaksanakan PKL internasional (di luar negeri) harus memperoleh izin orang tua, selain memenuhi persyaratan peserta PKL lainnya.

**Jawaban Pekael (1,81 detik):**

> Tentu, untuk kamu yang mau PKL di luar negeri atau PKL Internasional, ada syarat tambahan yang harus dipenuhi ya.
> Berikut adalah syarat tambahannya:
> • Memperoleh izin orang tua jika melaksanakan Praktik Kerja Lapangan (PKL) Internasional.
> Semoga informasi ini bisa membantu kelancaran persiapan PKL kamu, ya!

**Konteks yang ditemukan Pekael:** empat potongan teks, yaitu bagian persyaratan peserta PKL dari Buku Pedoman dan tiga potongan dari dokumen knowledge base tambahan tentang syarat dan tahapan PKL.

### 1. Faithfulness (kesetiaan jawaban pada sumber)

Pertanyaan yang dijawab metrik ini: apakah semua yang dikatakan Pekael benar-benar tertulis di konteks yang ditemukannya? Metrik ini mendeteksi jawaban yang mengarang.

Langkah 1, jawaban Pekael dipecah menjadi pernyataan-pernyataan tunggal:

| No | Pernyataan | Didukung konteks? | Alasan penilai |
|---|---|---|---|
| 1 | Mahasiswa yang ingin PKL di luar negeri harus memenuhi syarat tambahan | Ya | Konteks menyebut syarat tambahan untuk PKL internasional |
| 2 | Berikut adalah syarat tambahan | Tidak | Kalimat ini tidak ada di konteks |
| 3 | Mahasiswa harus memperoleh izin orang tua bila PKL internasional | Ya | Tertulis persis di konteks |
| 4 | Informasi tersebut diharapkan membantu kelancaran persiapan PKL | Tidak | Konteks tidak memuat pernyataan ini |

Langkah 2, nilai dihitung:

**Faithfulness = pernyataan yang didukung ÷ seluruh pernyataan = 2 ÷ 4 = 0,50**

Arti hasil ini: isi pokok jawaban (izin orang tua) benar, tetapi dua kalimat pengantar dan penutup yang bersifat basa-basi ikut dihitung sebagai pernyataan yang tidak ada di sumber.

### 2. Answer Relevancy (kesesuaian jawaban dengan pertanyaan)

Pertanyaan yang dijawab metrik ini: apakah jawaban Pekael benar-benar menjawab apa yang ditanyakan, tidak melenceng ke hal lain?

Caranya dibalik: penilai membaca jawaban Pekael lalu menebak pertanyaan apa yang cocok untuk jawaban itu, sebanyak tiga kali. Bila jawabannya tepat sasaran, tebakan pertanyaan akan mirip dengan pertanyaan asli. Kemiripan diukur dengan embedding, yaitu mengubah kalimat menjadi angka lalu membandingkan arahnya (*cosine similarity*, 1 berarti maknanya sama).

| Tebakan | Pertanyaan yang ditebak penilai | Kemiripan dengan pertanyaan asli |
|---|---|---|
| 1 | Apa syarat tambahan untuk melakukan PKL Internasional? | 0,951 |
| 2 | Apa syarat tambahan untuk melakukan PKL Internasional? | 0,951 |
| 3 | What additional requirement must be met for an international PKL? | 0,790 |

**Answer Relevancy = rata-rata kemiripan = (0,951 + 0,951 + 0,790) ÷ 3 = 0,897**

Penilai juga memeriksa apakah jawaban mengelak (misalnya "saya tidak tahu"). Bila ketiga tebakan menandai jawaban mengelak, nilainya menjadi 0. Pada contoh ini jawaban tidak mengelak. Nilai tebakan ketiga lebih rendah karena penilai menulisnya dalam bahasa Inggris, bukan karena jawaban Pekael melenceng.

### 3. Context Recall (kelengkapan sumber yang ditemukan)

Pertanyaan yang dijawab metrik ini: apakah potongan teks yang ditemukan Pekael sudah memuat semua informasi yang diperlukan untuk jawaban yang benar? Metrik ini menilai tahap pencarian, bukan tahap menjawab. Yang dibandingkan adalah jawaban acuan dengan konteks.

Langkah 1, jawaban acuan dipecah menjadi pernyataan, lalu setiap pernyataan dicari di konteks:

| No | Pernyataan jawaban acuan | Ada di konteks? | Alasan penilai |
|---|---|---|---|
| 1 | Mahasiswa PKL internasional harus memperoleh izin orang tua, selain memenuhi persyaratan peserta PKL lainnya | Ya | Konteks menyebut izin orang tua sebagai syarat tambahan PKL internasional bersama syarat peserta lainnya |

**Context Recall = pernyataan acuan yang ditemukan di konteks ÷ seluruh pernyataan acuan = 1 ÷ 1 = 1,00**

Arti hasil ini: pencarian Pekael sudah menemukan halaman yang tepat.

### Ringkasan contoh

| Metrik | Nilai | Yang dinilai | Kesimpulan untuk contoh ini |
|---|---|---|---|
| Faithfulness | 0,50 | Jawaban dibanding konteks | Isi benar, kalimat basa-basi menurunkan nilai |
| Answer Relevancy | 0,90 | Jawaban dibanding pertanyaan | Jawaban tepat sasaran |
| Context Recall | 1,00 | Konteks dibanding jawaban acuan | Sumber yang ditemukan sudah lengkap |

## Hasil 18 pertanyaan pertama

| No | Pertanyaan | Faithfulness | Answer Relevancy | Context Recall |
|---|---|---|---|---|
| 1 | Pengertian PKL | 1,00 | 0,89 | 1,00 |
| 2 | Dasar hukum PKL | 1,00 | 0,99 | 0,50 |
| 3 | Tujuan PKL | 0,80 | 0,88 | 1,00 |
| 4 | Manfaat PKL | 1,00 | 0,81 | 1,00 |
| 5 | Lama pelaksanaan | 0,80 | 0,98 | 1,00 |
| 6 | Jenis tempat PKL | 1,00 | 0,91 | 1,00 |
| 7 | Mengusulkan tempat sendiri | 1,00 | 0,89 | 1,00 |
| 8 | Penetapan tempat dan dosen pembimbing | 1,00 | 0,99 | 1,00 |
| 9 | Tugas dosen pembimbing | 1,00 | 0,85 | 1,00 |
| 10 | Tugas pembimbing lapangan | 0,88 | 0,88 | 1,00 |
| 11 | Kewajiban mahasiswa | 1,00 | 0,88 | 1,00 |
| 12 | Syarat minimal SKS | 1,00 | 1,00 | 1,00 |
| 13 | Mata kuliah prasyarat | 1,00 | 0,83 | 1,00 |
| 14 | PKL internasional | 0,50 | 0,90 | 1,00 |
| 15 | Syarat kelulusan | 0,33 | 0,85 | 1,00 |
| 16 | Kondisi harus mengulang | 0,90 | 0,96 | 1,00 |
| 17 | Tata tertib | 1,00 | 0,99 | 1,00 |
| 18 | Izin tidak hadir | 1,00 | 0,83 | 1,00 |
| | **Rata-rata** | **0,90** | **0,91** | **0,97** |

Seluruh 36 pertanyaan dijawab Pekael (status dijawab), dengan waktu jawab median 1,79 detik. Pertanyaan no. 19 sampai E6 sudah dijawab dan jawabannya tersimpan, tetapi belum dinilai.

## Temuan

1. **Kalimat basa-basi menurunkan Faithfulness.** Pada no. 3, 5, dan 14, kalimat pembuka atau penutup seperti "penting banget buat kamu pahami" dan "semoga informasi ini membantu" dihitung sebagai pernyataan yang tidak ada di sumber. Kalimat ini muncul karena gaya jawaban yang ramah (D-46, D-49). Isi pokok jawabannya benar.
2. **Penilai juga bisa keliru.** Pada no. 15, daftar syarat kelulusan yang dijawab Pekael dengan benar dibaca penilai sebagai pernyataan bahwa mahasiswa sudah memenuhi syarat tersebut, sehingga nilainya hanya 0,33. Sesuai spec, nilai rendah perlu diperiksa manual sebelum disimpulkan.
3. **Satu kekurangan pencarian yang nyata.** Pada no. 2 (dasar hukum PKL), konteks yang ditemukan tidak memuat Undang-Undang Nomor 20 Tahun 2003 dan Kepmendikbud Nomor 754/P/2020, sehingga Context Recall 0,50 dan jawaban Pekael hanya menyebut dua dari tiga peraturan.
4. **Bahasa tebakan pertanyaan memengaruhi Answer Relevancy.** Sebagian tebakan ditulis dalam bahasa Inggris sehingga kemiripannya lebih rendah walaupun maknanya sama.

## Kendala: kuota harian layanan penilai

Layanan Groq versi gratis membatasi model penilai sampai 200.000 token per hari dan 8.000 token per menit. Satu pertanyaan memerlukan sekitar 9.400 token, sehingga satu hari hanya cukup untuk sekitar 21 pertanyaan. Uji coba berhenti setelah pertanyaan ke-18. Penilaian sisa pertanyaan dapat dilanjutkan pada hari berikutnya tanpa meminta Pekael menjawab ulang, sehingga jawaban yang dinilai tetap sama. Hal yang sama berlaku untuk evaluasi akhir 38 pertanyaan pada Sprint 6, yang perlu dijadwalkan selama dua hari.

## Tindak lanjut

- Melanjutkan penilaian pertanyaan no. 19 sampai E6 setelah kuota Groq pulih.
- Membahas pada pembekuan pengaturan (S5-T07) apakah kalimat basa-basi perlu dikurangi pada gaya jawaban.
- Memeriksa manual setiap nilai di bawah 0,7 pada evaluasi akhir.
- Mengulang evaluasi dengan dataset yang sudah divalidasi *Product Owner*.

Rincian teknis, perintah, dan seluruh langkah perantara tercantum pada [log teknis uji coba Ragas](../../technical/ragas_dry_run.md).
