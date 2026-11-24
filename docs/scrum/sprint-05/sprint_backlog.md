# Sprint Backlog — Sprint 5

> Sprint Goal: Menghasilkan kandidat Pekael yang isinya sudah divalidasi *Product Owner*: knowledge base mencakup Buku Pedoman PKL dan dokumen knowledge base tambahan dari *Product Owner*, dataset evaluasi sekitar 30 pertanyaan beserta jawaban acuan telah divalidasi, pengaturan pencarian dan instruksi jawaban dibekukan untuk evaluasi akhir, dan uji coba evaluasi Ragas dengan layanan gratis berjalan.
> Status task: `To Do` · `In Progress` · `Done` · `Blocked`

## Task

| ID task | Item | Task | Status | Bukti (file / test / laporan) |
|---|---|---|---|---|
| S5-T01 | SUP-01 | Memeriksa ulang label halaman daftar topik pertanyaan (dibawa dari Sprint 4) | To Do | |
| S5-T02 | PBI-02, PBI-08 | Memasukkan dokumen knowledge base tambahan dari *Product Owner* dengan rujukan nama dokumen dan halaman | Done | D-53, EXP-010, [log teknis](../../technical/sprint-05.md) |
| S5-T03 | SUP-03 | Mengganti evaluator Ragas ke Groq versi gratis dan menguji ketiga metrik dengan satu contoh | In Progress | D-52, [smoke test](../../technical/smoke_tests.md) §8 |
| S5-T04 | SUP-01 | Menyusun dataset ground truth awal sekitar 30 pertanyaan beserta jawaban acuan dan konteks rujukan | To Do | |
| S5-T05 | SUP-01 | Validasi dataset bersama *Product Owner* | To Do | |
| S5-T06 | SUP-02 | Uji kasus angka, tanggal, persyaratan, parafrasa, multi-bagian, tidak tercakup, non-PKL, dan waktu jawab pagi, siang, malam | In Progress | EXP-010 |
| S5-T07 | SUP-02 | Kalibrasi dan pembekuan pengaturan untuk evaluasi akhir | To Do | |
| S5-T08 | SUP-03 | Uji coba Ragas pada beberapa entri dataset | To Do | |
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
