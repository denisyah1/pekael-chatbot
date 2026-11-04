# Lembar Validasi Sprint Report 3 — Bagian B: Sprint Review

| | |
|---|---|
| Sprint | : Sprint 3 |
| Periode Sprint | : 6 – 12 November 2026 |
| Tanggal *Sprint Review* | : 12 November 2026 |
| *Product Owner* (validator) | : Dosen Koordinator PKL Prodi PTIK UNJ |
| Scrum Master | : Dosen pembimbing |
| Developer | : Deni Merdiansyah (NIM {{NIM_DEVELOPER}}) |

## Tujuan

Lembar ini memuat hasil *Sprint Review* Sprint 3, yaitu Increment yang dihasilkan, untuk diperiksa dan divalidasi oleh *Product Owner* terhadap *Sprint Goal* dan kriteria selesai yang ditetapkan pada *Sprint Planning*.

## *Sprint Goal*

Menghasilkan alur tanya-jawab Pekael yang berjalan lengkap tanpa antarmuka: knowledge base tersimpan di FAISS dan dapat dimuat ulang, pertanyaan dicarikan potongan teks yang relevan, Gemini menyusun jawaban hanya dari potongan tersebut beserta rujukan halaman, dan pertanyaan di luar cakupan dijawab dengan pesan penolakan, sebagai dasar antarmuka Streamlit pada Sprint 4.

Status pencapaian: ☐ Tercapai ☐ Tercapai sebagian ☐ Tidak tercapai

## Increment yang dihasilkan

| No | Increment | Kriteria selesai | Hasil | Bukti |
|---|---|---|---|---|
| 1 | Knowledge base tersimpan di FAISS | Indeks dibangun dari halaman yang disetujui, dapat dimuat ulang pada proses baru, dan pembangunan yang gagal tidak mengganti indeks yang sedang dipakai | Knowledge base dibangun dari 19 halaman yang disetujui menjadi 33 potongan dalam sekitar 10 detik. Setiap kali perintah tanya-jawab dijalankan, knowledge base dimuat ulang dari penyimpanan tanpa dibangun ulang. Saat dibangun ulang, versi sebelumnya tetap disimpan sebagai cadangan. Pembangunan yang sengaja digagalkan (API key salah) tidak mengganti knowledge base yang sedang dipakai, dan Pekael tetap dapat menjawab | Logbook 8 dan 9 November, pengujian otomatis |
| 2 | Alur tanya-jawab tanpa antarmuka | Pertanyaan dalam cakupan dijawab berdasarkan buku panduan beserta rujukan halaman yang benar-benar diambil, pertanyaan di luar cakupan dijawab dengan pesan penolakan, gangguan layanan menampilkan pesan yang jelas | Dari 44 contoh pertanyaan: 35 dari 36 pertanyaan dalam cakupan dijawab dengan rujukan halaman, 5 pertanyaan PKL yang jawabannya tidak ada di buku dan 3 pertanyaan di luar topik PKL ditolak. Batas awal kedekatan 0,64 menolak pertanyaan di luar topik PKL sebelum Gemini dipanggil. Knowledge base yang belum ada, API key salah, kuota habis, layanan sibuk, dan pertanyaan kosong atau terlalu panjang menampilkan pesan yang jelas tanpa rincian teknis | Lembar Pemeriksaan Contoh Jawaban, catatan percobaan EXP-004 |

## Hasil pengujian

| Jenis pengujian | Cakupan | Hasil |
|---|---|---|
| Pengujian otomatis | Penyimpanan FAISS, penghubung Gemini, instruksi, enam langkah alur tanya-jawab, perakitan komponen, alur lengkap dengan pemuatan ulang, serta seluruh komponen sebelumnya | 224 lulus, 0 gagal |
| Uji langsung tanya-jawab | 44 contoh pertanyaan melalui alur lengkap | 35 dari 36 dijawab, 8 dari 8 pertanyaan di luar cakupan ditolak |
| Kalibrasi batas kedekatan (EXP-004) | Jarak potongan teratas pada 44 pertanyaan | Batas awal 0,64. Tidak ada pertanyaan dalam cakupan yang ditolak oleh batas, semua pertanyaan di luar topik PKL ditolak |
| Uji kondisi gagal | Knowledge base belum ada, API key salah, pertanyaan kosong dan terlalu panjang (langsung), kuota habis dan layanan sibuk (dengan tiruan layanan) | Semua menampilkan pesan yang aman |
| Uji pembangunan ulang | Bangun ulang dan bangun yang gagal | Versi lama tetap tersimpan, pembangunan yang gagal tidak mengganti knowledge base aktif |
| Waktu jawab | 44 pertanyaan | Umumnya sekitar 1,7 detik. 5 dari 36 pertanyaan dalam cakupan lebih dari 5 detik, paling lama 13 detik |

## Pekerjaan yang belum selesai

| Pekerjaan | Alasan | Tindak lanjut |
|---|---|---|
| Verifikasi koreksi OCR halaman 22–25 dan 27–28 (S3-T01) | Menunggu pemeriksaan Developer terhadap buku asli | Diselesaikan sebelum *Sprint Review*. Bila belum, dibawa ke Sprint 4 sebagai tugas pertama |

## Temuan dari pemeriksaan jawaban

| Temuan | Dampak | Tindak lanjut |
|---|---|---|
| Pertanyaan "tahapan setelah diterima di tempat PKL" ditolak, padahal prosedur pelaksanaan tercantum di halaman 14 | Satu pertanyaan dalam cakupan tidak terjawab | Diuji ulang bersama pengaturan jumlah potongan dan instruksi pada Sprint 5 |
| Jawaban "cara menghitung nilai akhir" belum memuat rumus 30% (N1) + 40% (N2) + 30% (N3) dari halaman 28 | Jawaban benar tetapi kurang lengkap | Diuji ulang bersama pengaturan jumlah potongan pada Sprint 5 |
| Model Gemini yang dipakai mengabaikan pengaturan agar jawaban selalu sama | Jawaban dapat sedikit berbeda setiap kali ditanya | Hasil evaluasi dicatat bersama tanggal, model, dan versi knowledge base |

## Masukan *Product Owner*

........................................................................................................................

........................................................................................................................

## Perubahan Product Backlog

| Perubahan | Alasan |
|---|---|
| Menambahkan uji ulang jumlah potongan yang diambil dan ukuran potongan pada Sprint 5 | Satu pertanyaan tidak terjawab dan satu jawaban kurang lengkap pada pemeriksaan Sprint 3 |
| Menguji ulang batas kedekatan dengan pertanyaan baru sebelum evaluasi akhir (Sprint 5) | Selisih jarak antara pertanyaan dalam cakupan dan pertanyaan di luar topik PKL hanya 0,08 |
| Menampilkan waktu tunggu dan pesan gangguan pada antarmuka Sprint 4 | Waktu jawab kadang lebih dari 5 detik, pesan status sudah tersedia dari alur tanya-jawab |

## Pernyataan validasi

Berdasarkan pemeriksaan terhadap Increment Sprint 3 pada lembar ini, *Product Owner* menyatakan Increment tersebut:

☐ Diterima
☐ Diterima dengan catatan: ........................................................................
☐ Belum diterima, pekerjaan dikembalikan ke Product Backlog

| | |
|---|---|
| Jakarta, 12 November 2026<br>*Product Owner* (Dosen Koordinator PKL),<br><br><br><br>Bambang Satrio, S. Pd., M. Kom.<br>NIP. {{NIP_PRODUCT_OWNER}} | <br>Developer,<br><br><br><br>Deni Merdiansyah<br>NIM {{NIM_DEVELOPER}} |

*Dasar penyusunan: Schwaber & Sutherland (2020) untuk komponen Sprint Review. Rujukan lengkap tercantum pada laporan.*
