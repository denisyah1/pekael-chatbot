# Sprint Backlog — Sprint 5

> Sprint Goal: Menghasilkan kandidat Pekael yang isinya sudah divalidasi *Product Owner*: knowledge base mencakup Buku Pedoman PKL dan dokumen knowledge base tambahan dari *Product Owner*, dataset evaluasi sekitar 30 pertanyaan beserta jawaban acuan telah divalidasi, pengaturan pencarian dan instruksi jawaban dibekukan untuk evaluasi akhir, dan uji coba evaluasi Ragas dengan layanan gratis berjalan.
> Status task: `To Do` · `In Progress` · `Done` · `Blocked`

## Task

| ID task | Item | Task | Status | Bukti (file / test / laporan) |
|---|---|---|---|---|
| S5-T01 | SUP-01 | Memeriksa ulang label halaman daftar topik pertanyaan (dibawa dari Sprint 4) | Done | Halaman sumber tercatat per pertanyaan di dataset evaluasi |
| S5-T02 | PBI-02, PBI-08 | Memasukkan dokumen knowledge base tambahan dari *Product Owner* dengan rujukan nama dokumen dan halaman | Done | D-53, EXP-010, [log teknis](../../technical/sprint-05.md) |
| S5-T03 | SUP-03 | Mengganti evaluator Ragas ke Groq versi gratis dan menguji ketiga metrik dengan satu contoh | Done | D-52, [smoke test](../../technical/smoke_tests.md) §8 |
| S5-T04 | SUP-01 | Menyusun dataset ground truth awal sekitar 30 pertanyaan beserta jawaban acuan dan konteks rujukan | Done | [dataset_ground_truth.md](dataset_ground_truth.md), D-56, D-57 |
| S5-T05 | SUP-01 | Validasi dataset bersama *Product Owner* | In Progress | Lembar validasi diserahkan |
| S5-T06 | SUP-02 | Uji kasus angka, tanggal, persyaratan, parafrasa, multi-bagian, tidak tercakup, non-PKL, dan waktu jawab pagi, siang, malam | In Progress | EXP-010, EXP-011 |
| S5-T07 | SUP-02 | Kalibrasi dan pembekuan pengaturan untuk evaluasi akhir | To Do | |
| S5-T08 | SUP-03 | Uji coba Ragas pada beberapa entri dataset | In Progress | [uji_coba_ragas.md](uji_coba_ragas.md), EXP-012 |
| S5-T09 | PBI-08 | Pengelolaan dokumen tambahan di ruang admin | In Progress | D-53 |
| S5-T10 | SUP-07 | Memeriksa enam pernyataan UAT pada Tabel 3.7 | To Do | |
| S5-T11 | SUP-04 | Perbandingan hosting dan estimasi biaya | To Do | |

## Log Pengerjaan

Satu entri per sesi kerja, ditulis setelah sesi selesai.

### 2026-11-20

**Dikerjakan**
- *Sprint Planning* Sprint 5 disusun dengan penanda tangan *Product Owner* ([sprint_planning.md](sprint_planning.md)).
- Dokumen knowledge base tambahan dari *Product Owner* diterima: 8 halaman teks digital (tidak memerlukan OCR) berisi butir tanya-jawab A1 sampai G3 tentang alur PKL, ketentuan waktu, rekognisi, penilaian, penulisan laporan, kontak resmi, dan batas jawaban chatbot. File disimpan di folder sumber yang tidak ikut ke repository karena memuat nomor kontak.
- Pekael kini dapat memakai lebih dari satu dokumen (S5-T02, D-53):
  - Buku Pedoman tetap memakai halaman yang disetujui, dokumen tambahan dipakai seluruhnya.
  - Setiap dokumen dipotong terpisah, sehingga satu potongan tidak pernah berisi dua dokumen.
  - Rujukan jawaban menyebut nama dokumen dan halaman PDF, dikelompokkan per dokumen.
  - Ruang admin menampilkan peta halaman per dokumen, dan dokumen tambahan selalu ikut saat buku dibangun ulang atau diganti.
- Knowledge base dibangun ulang: 27 halaman (19 halaman Buku Pedoman, 8 halaman dokumen tambahan) menjadi 61 potongan. Versi lama yang hanya berisi Buku Pedoman tetap tersimpan dan dapat diaktifkan kembali.
- Uji ulang 44 pertanyaan dengan knowledge base baru (EXP-010): 36 dari 36 pertanyaan dalam cakupan dijawab, pertanyaan cara menghitung nilai akhir kini memuat rumus 30% N1 + 40% N2 + 30% N3, dua pertanyaan yang dulu tidak ada di buku (margin dan huruf laporan, jadwal pembekalan) kini dijawab dari dokumen tambahan, ketiga pertanyaan non-PKL tetap ditolak. Waktu jawab median 1,68 detik, terlama 2,35 detik.
- Ditemukan dan diperbaiki: pembersih sapaan "Hai" di awal jawaban ikut menghapus kalimat pertama sampai tanda titik, sehingga jawaban "dijabat Bambang Satrio, S.Pd., M.Kom." terpotong menjadi "Pd., M.Kom." Kini hanya kata sapaannya yang dihapus (D-54).
- Evaluator Ragas diganti dari OpenAI (memerlukan kredit berbayar) ke Groq versi gratis (S5-T03, D-52). Tempat API key Groq disediakan di pengaturan lokal. Pemeriksa secret ditambah pola API key Groq. Uji ketiga metrik dijalankan dan berhenti dengan pesan bahwa API key Groq belum diisi.

**Hasil test**
- Pengujian otomatis: 340 lulus, 0 gagal (sebelumnya 327, bertambah 13 test untuk beberapa dokumen, evaluator Groq, dan sapaan).
- Uji Ragas: belum berjalan, menunggu API key Groq. Rincian di [smoke_tests.md](../../technical/smoke_tests.md) §8.

**File dibuat/diubah**
- Kode: pengaturan, pemuat PDF, `ChatbotManager`, penyimpanan FAISS, instruksi Gemini, halaman mahasiswa, ruang admin, skrip pembangunan knowledge base, skrip percobaan, skrip uji Ragas, pemeriksa secret.
- Test: `test_chatbot_manager.py`, `test_faiss_vector_store.py`, `test_pdf_loader.py`, `test_prompts.py`, `test_rag_steps.py`, `test_student_page.py`, `test_check_secrets.py`.
- Dokumen: `sprint_planning.md`, `sprint_backlog.md`, `decision_log.md`, `experiment_log.md`, `product_backlog.md`, `README.md`, `technical/sprint-05.md`, `technical/smoke_tests.md`.

**Keputusan**
- D-52 evaluator Ragas memakai Groq versi gratis.
- D-53 knowledge base beberapa dokumen.
- D-54 pembersih sapaan hanya menghapus kata sapaan.

**Hambatan**
- API key Groq belum diisi, sehingga uji ketiga metrik Ragas belum berjalan.
- Dokumen tambahan masih memuat isian kontak Koordinator PKL berupa keterangan ("Kontak Koordinator, email institusi, WhatsApp dan jam layanan"), belum berupa nomor atau alamat email. Perlu dilengkapi *Product Owner*.
- Nomor halaman yang tercetak di dokumen tambahan (Halaman 2 sampai 9) berbeda dengan nomor halaman PDF (1 sampai 8). Rujukan memakai nomor halaman PDF, sama seperti Buku Pedoman.
- Jawaban jadwal pembekalan memakai kalimat dokumen tambahan tentang jadwal seminar dan laporan ("diumumkan oleh admin prodi atau Koorprodi"). Perlu diperiksa *Product Owner* saat validasi isi.

**Berikutnya**
- Mengisi API key Groq lalu menjalankan uji ketiga metrik Ragas.
- Memeriksa ulang label daftar topik (S5-T01) dan mulai menyusun dataset evaluasi (S5-T04).

### 2026-11-21

**Dikerjakan**
- API key Groq diisi Developer di pengaturan lokal. Uji ketiga metrik Ragas dengan satu contoh fiktif berhasil: Faithfulness 1,000, Answer Relevancy 0,992, Context Recall 1,000, masing-masing 2 sampai 7 detik (S5-T03 selesai). Evaluator Groq versi gratis dapat dipakai untuk uji coba Ragas pada dataset.
- Developer melaporkan pertanyaan "siapa koordinator PKL" berstatus di luar cakupan. Penyebab: Gemini menjawab benar dengan nama Koordinator PKL, lalu mengutip tugas koordinator dari dokumen tambahan ("pertanyaan PKL yang jawabannya tidak ada di panduan"). Kalimat itu terbaca sebagai pengakuan bahwa informasinya tidak ada, sehingga jawaban diganti kalimat arahan siap pakai. Kini kalimat yang didahului "yang" atau "jawabannya" tidak lagi dihitung sebagai pengakuan (D-55).
- Uji langsung pertanyaan yang sama dengan tiga gaya: ketiganya dijawab dengan nama Koordinator PKL. Dua jawaban diawali sisa sapaan ("Kamu, ...", "Juga! ...") dari "Hai kamu" dan "Halo juga". Kata yang menempel pada sapaan kini ikut dihapus (lanjutan D-54).
- Uji ulang 44 pertanyaan (EXP-011): 36 dari 36 pertanyaan dalam cakupan dijawab, pertanyaan koordinator PKL dijawab, pertanyaan jadwal pembekalan kini diarahkan ke Admin Prodi PTIK, pertanyaan non-PKL tetap ditolak. Waktu jawab median 1,67 detik.

**Hasil test**
- Pengujian otomatis: 342 lulus, 0 gagal (bertambah 2 test).
- Uji Ragas: 3 dari 3 metrik berjalan. Rincian di [smoke_tests.md](../../technical/smoke_tests.md) §8.

**File dibuat/diubah**
- Kode: instruksi dan pemeriksaan jawaban (`prompts.py`).
- Test: `test_prompts.py`.
- Dokumen: `sprint_backlog.md`, `decision_log.md`, `experiment_log.md`, `technical/sprint-05.md`, `technical/smoke_tests.md`.

**Keputusan**
- D-55 kalimat yang menggambarkan jenis pertanyaan lain tidak dianggap arahan.

**Hambatan**
- Satu jawaban memerlukan 9,28 detik pada EXP-011, jawaban lainnya di bawah 2,5 detik.

**Berikutnya**
- Memeriksa ulang label daftar topik (S5-T01) dan menyusun dataset evaluasi (S5-T04).

### 2026-11-22

**Dikerjakan**
- Dataset evaluasi versi v1 disusun (S5-T04, D-56): 40 pertanyaan, terdiri atas 36 pertanyaan uji Sprint 4 dengan jawaban acuan dan 4 pertanyaan di luar PKL dengan perilaku yang diharapkan. Dataset ini dipakai untuk evaluasi Ragas dan seluruh pengujian berikutnya.
- Jawaban acuan ditulis dari teks Buku Pedoman yang sudah diperiksa dan dokumen knowledge base tambahan. Setiap pertanyaan menyimpan halaman sumber dan teks halaman tersebut sebagai konteks rujukan. Pemeriksaan ulang halaman sumber ini menyelesaikan S5-T01 tanpa mengubah dokumen Sprint 1.
- Lembar validasi untuk *Product Owner* dibuat tanpa menampilkan halaman sumber ([dataset_ground_truth.md](dataset_ground_truth.md)). Setiap pertanyaan diberi pilihan "Sesuai" atau "Perlu perbaikan" dengan catatan. Tiga pertanyaan diberi catatan penyusun karena memerlukan keputusan *Product Owner*: alur pengajuan dan tempat pendaftaran yang memuat praktik di PTIK, perhitungan menit per minggu, dan versi sistematika laporan.
- Dataset dan lembar validasi dihasilkan dari satu skrip, sehingga perbaikan dari *Product Owner* cukup diterapkan sekali lalu keduanya dibuat ulang.

**Hasil test**
- Pengujian otomatis: 344 lulus, 0 gagal (bertambah 2 test untuk dataset: 40 nomor unik, teks pertanyaan sama dengan daftar Sprint 4, setiap jawaban punya sumber, lembar tanpa halaman sumber).

**File dibuat/diubah**
- Skrip: `build_ground_truth.py` (baru), `export_docs.py` (judul lampiran dataset).
- Test: `test_ground_truth.py` (baru).
- Dokumen: `dataset_ground_truth.md` (baru), `sprint_backlog.md`, `decision_log.md`, `technical/sprint-05.md`.

**Keputusan**
- D-56 susunan dataset evaluasi 40 pertanyaan.

**Hambatan**
- Tidak ada.

**Berikutnya**
- Validasi lembar dataset oleh *Product Owner* (S5-T05) pada 23 November 2026.

### 2026-11-23

**Dikerjakan**
- Lembar Product Backlog utama disusun atas permintaan Developer ([sprint-01/product_backlog_utama.md](../sprint-01/product_backlog_utama.md)): delapan item PBI-01 sampai PBI-08 dari proposal dan rencana implementasi beserta prioritas, sprint, kriteria penerimaan, bukti hasil, rencana sprint, Definition of Done, dan aturan perubahan. Lembar diberi tanggal 23 Oktober 2026 karena menjadi acuan sejak *Sprint Planning* Sprint 1, dan ditempatkan di folder Sprint 1 tanpa mengubah dokumen Sprint 1 yang sudah ada.
- Skrip ekspor dokumen diberi pilihan untuk mengekspor satu dokumen saja, sehingga file Word dan PDF Sprint 1 yang sudah diedit tidak tertimpa.

**Hasil test**
- Pengujian otomatis: 344 lulus, 0 gagal.

**File dibuat/diubah**
- Dokumen: `sprint-01/product_backlog_utama.md` (baru), `sprint_backlog.md`.
- Skrip: `export_docs.py`.

**Hambatan**
- Tidak ada.

**Berikutnya**
- Validasi lembar dataset oleh *Product Owner* (S5-T05) dan uji coba Ragas (S5-T08).

### 2026-11-24

**Dikerjakan**
- Dataset evaluasi diperbaiki menjadi versi v2 atas permintaan Developer (D-57): isinya kini sama dengan 44 pertanyaan yang diujikan sejak Sprint 3 dan Sprint 4, menggantikan susunan 40 pertanyaan versi v1.
  - 36 pertanyaan dalam cakupan tetap dengan jawaban acuan yang sama.
  - L4 (Koordinator PKL Prodi PTIK) dan L5 (format margin dan huruf laporan) dulu tidak ada di Buku Pedoman, kini diberi jawaban acuan dari dokumen knowledge base tambahan.
  - L1 (batas pendaftaran), L2 (jadwal pembekalan), dan L3 (lowongan perusahaan) tidak ada di kedua dokumen, sehingga diisi perilaku yang diharapkan: tidak menebak dan mengarahkan ke pihak prodi yang tepat.
  - N1 sampai N3 tetap sebagai pertanyaan di luar PKL. Pertanyaan tambahan N4 pada versi v1 dihapus.
- Lembar validasi untuk *Product Owner* dibuat ulang dengan tiga kelompok: 38 pertanyaan dengan jawaban acuan, 3 pertanyaan yang diarahkan, dan 3 pertanyaan di luar PKL.

**Hasil test**
- Pengujian otomatis: 344 lulus, 0 gagal. Test dataset kini memeriksa 44 nomor unik dan kesamaan teks pertanyaan dengan pertanyaan percobaan.

**File dibuat/diubah**
- Skrip: `build_ground_truth.py`.
- Test: `test_ground_truth.py`.
- Dokumen: `dataset_ground_truth.md`, `sprint_backlog.md`, `decision_log.md`, `technical/sprint-05.md`.

**Keputusan**
- D-57 dataset evaluasi memakai 44 pertanyaan pengujian.

**Hambatan**
- Tidak ada.

**Berikutnya**
- Validasi lembar dataset oleh *Product Owner* (S5-T05), lalu uji coba Ragas (S5-T08).

### 2026-11-25

**Dikerjakan**
- Skrip evaluasi Ragas dibuat sesuai rancangan spec (S5-T08): Pekael menjawab setiap pertanyaan seperti saat dipakai mahasiswa, jawaban dan potongan teks yang ditemukan disimpan, lalu dinilai dengan Faithfulness, Answer Relevancy, dan Context Recall. Setiap langkah perantara penilaian (pernyataan, alasan penilai, tebakan pertanyaan, kemiripan) ikut disimpan sehingga setiap nilai dapat dijelaskan.
- Uji integrasi pada dua pertanyaan menemukan jawaban penilai untuk Faithfulness terpotong. Batas panjang keluaran penilai dinaikkan (D-58).
- Uji coba pada 36 pertanyaan uji (EXP-012): seluruh pertanyaan dijawab Pekael, 18 pertanyaan pertama selesai dinilai dengan rerata Faithfulness 0,90, Answer Relevancy 0,91, dan Context Recall 0,97. Penilaian berhenti karena kuota token harian layanan penilai tercapai.
- Laporan uji coba berbahasa sederhana dengan satu contoh pertanyaan yang dijelaskan per metrik disusun ([uji_coba_ragas.md](uji_coba_ragas.md)).

**Hasil test**
- Pengujian otomatis: 351 lulus, 0 gagal (bertambah 7 test modul evaluasi).
- Uji coba Ragas: 18 dari 36 pertanyaan dinilai, 18 menunggu kuota.

**File dibuat/diubah**
- Kode: `evaluation/dataset.py`, `evaluation/ragas_evaluator.py` (baru).
- Skrip: `run_ragas_evaluation.py` (baru), `export_docs.py`.
- Test: `test_evaluation.py` (baru).
- Dokumen: `uji_coba_ragas.md` (baru), `technical/ragas_dry_run.md` (baru), `sprint_backlog.md`, `decision_log.md`, `experiment_log.md`, `README.md`.

**Keputusan**
- D-58 pengaturan evaluator dan pembagian evaluasi menjadi dua hari.

**Hambatan**
- Kuota gratis Groq 200.000 token per hari hanya cukup untuk sekitar 21 pertanyaan per hari.

**Berikutnya**
- Melanjutkan penilaian no. 19 sampai E6 setelah kuota pulih.
