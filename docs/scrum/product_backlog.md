# Product Backlog — Pekael

> Sumber: proposal skripsi (Tabel Product Backlog) dan `project_spec.md` §13.
> Product Owner: Bambang Satrio, S. Pd., M. Kom. · Terakhir diperbarui: 2026-11-13

## Item Product Backlog (dari proposal)

| ID | Item | Prioritas | Sprint | Kriteria penerimaan | Status |
|---|---|---|---|---|---|
| PBI-01 | Ekstraksi teks dari buku panduan PKL hasil scan melalui OCR | Tinggi | 1 | Teks per halaman tersedia dengan metadata halaman dan metode ekstraksi, OCR hanya untuk halaman tanpa teks digital, sampel angka/tanggal/tabel sudah diperiksa terhadap sumber asli | Diterima PO |
| PBI-02 | Penyaringan dan pengerucutan konten sesuai lingkup PTIK | Tinggi | 1 | Knowledge base terpilih dan disetujui PO secara tertulis | Diterima PO |
| PBI-03 | Text splitting dan embedding menjadi representasi vektor | Tinggi | 2 | Chunk mempertahankan metadata source/page, dimensi vektor konsisten, eksperimen parameter tercatat | Dikerjakan |
| PBI-04 | Penyimpanan embedding pada FAISS | Tinggi | 3 | Indeks `IndexFlatL2` dapat dibuat, disimpan, dan dimuat ulang pada proses baru | Diterima PO |
| PBI-05 | Retrieval chain menghubungkan FAISS dan Gemini API | Tinggi | 3 | Pipeline CLI menghasilkan jawaban beserta sumber, fallback berjalan untuk pertanyaan di luar cakupan | Diterima PO |
| PBI-06 | Antarmuka website untuk tanya-jawab | Tinggi | 4 | UI Streamlit menerima pertanyaan, menampilkan loading, jawaban, dan status error yang aman | Dikerjakan |
| PBI-07 | Penampilan rujukan sumber pada setiap jawaban | Sedang | 4 | Nama dokumen dan halaman PDF tampil hanya dari chunk yang benar-benar diambil | Dikerjakan |
| PBI-08 | Admin mengunggah/memperbarui dokumen knowledge base | Sedang | 4 | Login satu admin, upload PDF, indeks lama tetap aktif jika build gagal | Dikerjakan |

## Pekerjaan Pendukung Sprint 5–6

Item berikut adalah aktivitas validasi dan evaluasi menurut spec §12. Item ini **bukan** tambahan PBI pada proposal.

| ID | Aktivitas | Sprint | Status |
|---|---|---|---|
| SUP-01 | Dataset ground truth dan validasi oleh PO | 5 | Belum dimulai |
| SUP-02 | Kalibrasi dan pembekuan parameter (k, threshold, chunking, prompt) | 5 | Belum dimulai |
| SUP-03 | Dry-run Ragas | 5 | Belum dimulai |
| SUP-04 | Pemilihan hosting dan estimasi biaya | 5 | Belum dimulai |
| SUP-05 | Deployment dan smoke test di lingkungan target | 6 | Belum dimulai |
| SUP-06 | Evaluasi Ragas final (3 metrik) | 6 | Belum dimulai |
| SUP-07 | UAT minimal 100 responden dan analisis | 6 | Belum dimulai |

Nilai status: `Belum dimulai` · `Dikerjakan` · `Selesai (menunggu review)` · `Diterima PO` · `Ditunda`

## Riwayat Perubahan

| Tanggal | Perubahan | Alasan | Disetujui oleh |
|---|---|---|---|
| 2026-10-23 | Product Backlog awal disusun dari proposal | Awal proyek | PO |
| 2026-10-23 | PBI-01 dan PBI-02 direncanakan untuk Sprint 1 (23–29 Okt 2026). Pemeriksaan awal: Buku Pedoman PKL 2025 berisi 29 halaman, seluruhnya hasil scan | Sprint 1 Planning | PO (validasi planning Sprint 1, tanda tangan fisik menyusul) |
| 2026-10-30 | PBI-03 dimulai pada Sprint 2 (30 Okt – 5 Nov 2026). Penyelesaian PBI-02 (keputusan penyaringan) dibawa ke Sprint 2 | Sprint 2 Planning | PO |
| 2026-10-29 | Sprint 1 diterima PO. PBI-02 selesai: knowledge base memakai halaman 4–16, 22–25, 27–28. Halaman 22–25 (sistematika laporan) dan 27–28 (instrumen penilaian) menambah ruang lingkup proposal. PBI-01 berlanjut di Sprint 2 untuk pemeriksaan OCR halaman tambahan | Sprint 1 Review | PO |
| 2026-11-06 | PBI-04 dan PBI-05 dimulai pada Sprint 3 (6 – 12 Nov 2026). Pemeriksaan OCR halaman 22–25 dan 27–28 (lanjutan PBI-01) dibawa dari Sprint 2 | Sprint 3 Planning | PO |
| 2026-11-12 | Sprint 3 diterima PO. PBI-01 selesai (OCR seluruh halaman knowledge base terverifikasi), PBI-04 dan PBI-05 selesai. Uji ulang jumlah potongan, ukuran potongan, dan batas kedekatan dicatat untuk Sprint 5 (SUP-02) | Sprint 3 Review | PO |
| 2026-11-13 | PBI-06, PBI-07, dan PBI-08 dimulai pada Sprint 4 (13 – 26 Nov 2026) | Sprint 4 Planning | PO |
