# Fase Setup

> **Periode:** 23 Oktober 2026
> **Status:** Selesai, dengan satu pekerjaan tertunda (uji evaluator OpenAI, menunggu saldo API)
> **Rincian teknis:** [`docs/technical/setup_log.md`](../technical/setup_log.md) · [`docs/technical/smoke_tests.md`](../technical/smoke_tests.md)

## Apa itu fase Setup?

Fase Setup adalah tahap persiapan sebelum Sprint 1. Tujuannya menyiapkan "bengkel kerja": memasang perangkat lunak yang dibutuhkan, menyusun kerangka program, dan memastikan setiap alat benar-benar bisa dipakai. Fitur chatbot belum dibuat pada tahap ini, fitur dibangun bertahap pada Sprint 1–6.

## Ringkasan Pekerjaan

| No | Pekerjaan | Hasil |
|---|---|---|
| 1 | Menyusun rencana implementasi | `implementation_plan.md` disetujui pemilik proyek |
| 2 | Memasang Python 3.11 | Terpasang (3.11.9) |
| 3 | Memasang Tesseract OCR dan bahasa Indonesia | Terpasang (5.4.0), bahasa `ind` dan `eng` tersedia |
| 4 | Menyusun struktur folder dan kerangka program | Sesuai rancangan class diagram proposal |
| 5 | Memasang dan mengunci versi library | Versi semua library dicatat agar lingkungan dapat dibuat ulang persis sama |
| 6 | Menyiapkan file konfigurasi | Pengaturan (model, ukuran chunk, dsb.) dapat diubah tanpa menyentuh kode |
| 7 | Membuat kelas inti dan pola Abstract Factory | Loader, splitter, dan vector store dibuat lewat factory sesuai proposal |
| 8 | Menulis pengujian otomatis | **65 test lulus, 0 gagal** |
| 9 | Menguji koneksi ke Gemini | Berhasil (chat dan embedding) |
| 10 | Menguji Ragas | Sebagian: bagian Gemini berhasil, bagian OpenAI tertunda |
| 11 | Pengaman agar API key tidak ikut ter-upload | Aktif dan sudah diuji |
| 12 | Panduan instalasi (README) | Selesai |

## Hasil Uji Coba Awal (Smoke Test)

Smoke test adalah uji singkat untuk memastikan setiap alat bisa "menyala" sebelum dipakai membangun sistem.

| Yang diuji | Hasil | Arti sederhananya |
|---|---|---|
| Penyimpanan vektor FAISS | Berhasil | Tempat menyimpan "sidik makna" potongan buku panduan siap dipakai |
| Pembaca PDF (PyMuPDF) | Berhasil | Teks di dalam PDF bisa dibaca per halaman |
| OCR bahasa Indonesia (Tesseract) | Berhasil | Halaman hasil scan bisa diubah menjadi teks |
| Model Gemini (`gemini-3.5-flash-lite`) | Berhasil (percobaan ke-2) | Chatbot bisa menyusun jawaban dalam Bahasa Indonesia |
| Embedding Gemini (`gemini-embedding-001`) | Berhasil | Teks bisa diubah menjadi vektor 768 angka untuk pencarian |
| Ragas dengan embedding Gemini | Berhasil | Metrik Answer Relevancy bisa memakai Gemini, tanpa biaya embedding OpenAI |
| Ragas dengan evaluator OpenAI (`gpt-4o-mini`) | **Tertunda** | Saldo akun OpenAI masih kosong |

## Kendala dan Penyelesaiannya

| Kendala | Penyelesaian |
|---|---|
| Library `langchain-community` (wadah FAISS untuk LangChain) sudah tidak dikembangkan lagi oleh pembuatnya | Versi yang terbukti berfungsi dikunci. Paket "pengganti" yang beredar ternyata tidak resmi, jadi tidak dipakai. Keputusan jangka panjang dibahas di Sprint 3 |
| Versi terbaru `langchain-community` membuat Ragas gagal dijalankan | Diturunkan satu versi (0.4.2 → 0.4.1), semua test tetap lulus |
| API key sempat tertulis di file contoh dan masuk commit lokal | Terdeteksi GitHub sebelum ter-upload, jadi **tidak bocor ke publik**. Riwayat commit dibersihkan, key dianjurkan diganti, dan dipasang pengaman otomatis agar tidak terulang |
| Server Gemini sempat sibuk (error 503) | Berhasil pada percobaan kedua. Menjadi catatan agar aplikasi menampilkan pesan yang ramah saat hal ini terjadi |
| Saldo API OpenAI kosong | Menunggu pemilik proyek mengisi saldo, pekerjaan lain tetap berjalan |

## Catatan untuk Sprint Berikutnya

- Satu kali uji chat Gemini memakan waktu sekitar 5 detik, padahal target kuesioner UAT di bawah 5 detik. Waktu respons akan diukur ulang setelah sistem lengkap (Sprint 5).
- Vektor dari Gemini perlu dinormalisasi sebelum disimpan di FAISS agar ambang batas relevansi lebih stabil. Rencana ini diuji di Sprint 2.

## Pekerjaan Tertunda

| Pekerjaan | Menunggu | Dikerjakan oleh |
|---|---|---|
| Uji ketiga metrik Ragas dengan evaluator OpenAI | Saldo API OpenAI | Pemilik mengisi saldo, lalu Claude Code menjalankan `scripts/smoke_test_ragas.py` |
| Mengisi `TESSERACT_CMD` di `.env` | — | Pemilik proyek (sebelum Sprint 1) |
| Mengaktifkan pengaman commit (`git config core.hooksPath .githooks`) | — | Pemilik proyek |

## Keputusan yang Diambil

Daftar lengkap ada di [`docs/decision_log.md`](../decision_log.md) (D-01 s.d. D-18).
