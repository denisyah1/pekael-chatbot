# Hasil Smoke Test

Smoke test memastikan setiap komponen dapat dipanggil sebelum pipeline dibangun. Spec §9.1 dan §10.4 mewajibkan hasilnya disimpan beserta model ID dan versi yang dipakai. Hasil yang sudah dicatat tidak diubah, uji ulang ditambahkan sebagai baris baru.

## Lingkungan

| | |
|---|---|
| OS | Windows 11 Home Single Language 10.0.26300 |
| Python | 3.11.9 (`.venv`) |
| Versi paket | `requirements-lock.txt` |

## 1. Lingkungan lokal (tanpa API)

Perintah: `.venv\Scripts\python.exe -m pytest tests/unit/test_environment.py -v`

| Tanggal | Test | Hasil |
|---|---|---|
| 2026-10-23 | Import semua paket inti | Lulus |
| 2026-10-23 | Aplikasi tidak memuat paket evaluator | Lulus |
| 2026-10-23 | FAISS `IndexFlatL2` 768 dimensi: buat, simpan, muat ulang, cari | Lulus |
| 2026-10-23 | PyMuPDF: ekstraksi teks dan render halaman | Lulus |
| 2026-10-23 | Tesseract 5.4.0 dengan bahasa `ind`: OCR teks "PRAKTIK KERJA LAPANGAN" | Lulus |
| 2026-10-23 | Ragas 0.4.3: import ketiga metrik, LLM factory, GoogleEmbeddings | Lulus |

## 2. Gemini (API sungguhan)

Perintah: `.venv\Scripts\python.exe scripts\smoke_test_models.py` (tanpa retry)

| Tanggal | Percobaan | Uji | Model | Hasil | Waktu | Catatan |
|---|---|---|---|---|---|---|
| 2026-10-23 | 1 | Chat | `gemini-3.5-flash-lite` | **Gagal** | 2,65 s | `503 UNAVAILABLE`: model sedang ramai ("high demand"). Model ID dan API key valid |
| 2026-10-23 | 1 | Embedding dokumen | `gemini-embedding-001` | Lulus | 1,74 s | `RETRIEVAL_DOCUMENT`, dimensi 768, norma L2 0,5839 |
| 2026-10-23 | 1 | Embedding query | `gemini-embedding-001` | Lulus | 1,63 s | `RETRIEVAL_QUERY`, dimensi 768, norma L2 0,5908 |
| 2026-10-23 | 2 | Chat | `gemini-3.5-flash-lite` | Lulus | 5,01 s | Jawaban: *"Dalam konteks perkuliahan, PKL adalah singkatan dari Praktik Kerja Lapangan."* |
| 2026-10-23 | 2 | Embedding dokumen | `gemini-embedding-001` | Lulus | 1,66 s | dimensi 768, norma L2 0,5839 |
| 2026-10-23 | 2 | Embedding query | `gemini-embedding-001` | Lulus | 1,81 s | dimensi 768, norma L2 0,5908 |

**Temuan**
1. `gemini-3.5-flash-lite` tersedia untuk API key ini dan menjawab dalam Bahasa Indonesia (OD-01).
2. Error `503` dapat terjadi kapan saja. Pipeline (Sprint 3) harus menampilkan pesan yang ramah dan tidak menganggapnya sebagai jawaban (NFR-04, FR-08).
3. Waktu chat 5,01 s untuk prompt pendek, **tanpa** retrieval. Butir UAT no. 1 menargetkan < 5 detik, jadi latensi perlu diukur ulang pada pipeline lengkap (Sprint 5). Satu pengukuran belum cukup untuk menarik kesimpulan.
4. Embedding 768 dimensi **tidak** ternormalisasi (norma ≈ 0,58–0,59). Ini mendukung rencana normalisasi L2 sebelum FAISS (D-05/OD-12).

## 3. Ragas (API sungguhan)

Perintah: `.venv\Scripts\python.exe scripts\smoke_test_ragas.py` (1 sampel fiktif, bukan data penelitian)

| Tanggal | Metrik | Evaluator LLM | Embedding | Hasil | Catatan |
|---|---|---|---|---|---|
| 2026-10-23 | Faithfulness | `gpt-4o-mini` | — | **Gagal** | `429 insufficient_quota`: saldo kredit OpenAI kosong |
| 2026-10-23 | Answer Relevancy | `gpt-4o-mini` | `gemini-embedding-001` | **Gagal** | sama |
| 2026-10-23 | Context Recall | `gpt-4o-mini` | — | **Gagal** | sama |
| 2026-10-23 | Komponen embedding Ragas (`GoogleEmbeddings.aembed_text`) | — | `gemini-embedding-001` | Lulus | dimensi 3072 (default), norma 1,0 |

**Temuan**
1. API key OpenAI valid (error 429 kuota, bukan 401 key ditolak), tetapi akun belum memiliki kredit. Verifikasi evaluator (OD-06) **tertunda** sampai pemilik mengisi saldo.
2. Embedding Gemini kompatibel dengan Ragas 0.4.3, jadi `text-embedding-3-small` tidak diperlukan (OD-05).
3. Dimensi embedding untuk Answer Relevancy (3072) terpisah dari dimensi indeks FAISS. Metrik ini hanya membandingkan pertanyaan dengan pertanyaan, jadi tidak memengaruhi indeks.

## 4. Embedding melalui wrapper Pekael (Sprint 2)

| Tanggal | Uji | Hasil | Catatan |
|---|---|---|---|
| 2026-10-30 | `GeminiEmbeddings.embed_documents` + `embed_query` | Lulus | dimensi 768, norma 1,0000, 1,19 s |
| 2026-10-30 | Masukan 9.000 karakter | Diterima | 0,52 s |
| 2026-10-30 | Masukan 40.000 karakter | Diterima tanpa galat | Indikasi pemotongan diam-diam oleh layanan, wrapper kini menolak > 8.000 karakter |

## 5. Prompt jawaban Gemini (Sprint 3)

| Tanggal | Uji | Hasil | Catatan |
|---|---|---|---|
| 2026-11-07 | Pertanyaan dengan jawaban di konteks | Lulus | Jawaban sesuai buku, rujukan hal. 10, 3,80 s |
| 2026-11-07 | Pertanyaan PKL tanpa jawaban di buku | Lulus | `TIDAK_DITEMUKAN`, 9,75 s |
| 2026-11-07 | Pertanyaan yang butuh dua bagian buku | Lulus | Rujukan hal. 16 dan 11, 9,61 s |
| 2026-11-07 | `thinking_budget=0` | Ditolak model | `400 INVALID_ARGUMENT` |

## 6. Alur tanya-jawab lengkap dari terminal (Sprint 3)

Perintah: `scriptsuild_knowledge_base.py`, lalu `scriptssk.py "<pertanyaan>"`. Indeks `20261102T180419398924-565a9929` (19 halaman, 33 potongan, 10,4 s).

| Tanggal | Uji | Hasil | Catatan |
|---|---|---|---|
| 2026-11-08 | Membangun knowledge base | Lulus | 33 potongan, 768 dimensi, satu panggilan embedding |
| 2026-11-08 | Syarat SKS (langsung dan parafrasa "90 SKS") | Lulus | Rujukan hal. 10, 2,33 s dan 1,32 s |
| 2026-11-08 | Nilai 74 (dua bagian buku) | Lulus | Rujukan hal. 16 dan 11 |
| 2026-11-08 | Bobot N2 (halaman tambahan) | Lulus | "40%", rujukan hal. 28 |
| 2026-11-08 | Dokumen lampiran laporan | Lulus | 8 dokumen a–h, rujukan hal. 24 |
| 2026-11-08 | Batas pendaftaran (tidak ada di buku) | Lulus | Ditolak oleh prompt |
| 2026-11-08 | Non-PKL (nasi goreng, machine learning) | Lulus | Ditolak ambang 0,64 tanpa memanggil Gemini, 0,75 s |
| 2026-11-08 | Folder indeks kosong | Lulus | Status `unavailable`, "Knowledge base Pekael belum disiapkan" |
| 2026-11-08 | API key tidak valid | Lulus | Status `unavailable`, "belum dikonfigurasi dengan benar", key tidak tercetak |
| 2026-11-08 | Pertanyaan kosong dan 501 karakter | Lulus | Status `invalid_input`, tanpa panggilan API |
| 2026-11-09 | Bangun ulang knowledge base | Lulus | Build baru aktif, build lama tetap tersimpan (2 versi) |
| 2026-11-09 | Bangun dengan API key tidak valid | Lulus | Gagal dengan pesan aman, `ACTIVE` tidak berubah, pertanyaan sesudahnya tetap dijawab |

Kuota habis dan timeout tidak dipicu secara langsung, keduanya diuji dengan tiruan di `tests/unit/test_rag_steps.py`.

## 7. Kecepatan model Gemini (Sprint 4)

| Tanggal | Model | Hasil | Catatan |
|---|---|---|---|
| 2026-11-15 | `gemini-3.5-flash-lite` | 10,72–44,15 s, satu `504 DEADLINE_EXCEEDED` | Pertanyaan satu kata, tanpa konteks |
| 2026-11-15 | `gemini-3.5-flash` | 3,45–5,30 s | Pertanyaan yang sama |
| 2026-11-15 | `gemini-2.5-flash-lite`, `gemini-2.5-flash` | `404 NOT_FOUND` | Tidak tersedia untuk pengguna baru |
| 2026-11-15 | `gemini-3.5-flash` (alur lengkap, EXP-005) | 13/36 dijawab, lalu 429 | Kuota gratis 20 permintaan per hari |
| 2026-11-15 | `gemini-3.5-flash-lite` (alur lengkap, per langkah) | Gemini 22,8–28,8 s, pencarian 0,5 s | Hampir seluruh waktu di Gemini |
| 2026-11-15 | `gemini-3.5-flash-lite` (streaming) | Token pertama 13,91 s, selesai 14,07 s | Menunggu sebelum token pertama |
