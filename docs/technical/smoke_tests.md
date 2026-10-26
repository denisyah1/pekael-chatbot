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
