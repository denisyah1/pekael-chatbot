# Pekael

Chatbot berbasis Retrieval-Augmented Generation (RAG) menggunakan LangChain untuk layanan informasi Praktik Kerja Lapangan (PKL) mahasiswa Prodi Pendidikan Teknik Informatika dan Komputer (PTIK), Universitas Negeri Jakarta.

Pekael menjawab pertanyaan mahasiswa **hanya** berdasarkan buku panduan PKL resmi yang telah divalidasi, dan menampilkan rujukan halaman sumber pada setiap jawaban berbasis dokumen.

| Komponen | Teknologi |
|---|---|
| Bahasa | Python 3.11 |
| Framework RAG | LangChain |
| Model generatif | Google Gemini API |
| Embedding | `gemini-embedding-001` |
| Vector store | FAISS (`IndexFlatL2`, CPU) |
| Ekstraksi PDF / OCR | PyMuPDF / Tesseract OCR |
| Antarmuka | Streamlit |
| Evaluasi | Ragas (Faithfulness, Answer Relevancy, Context Recall) + UAT |

> **Status:** fase Setup. Pipeline RAG dan UI dibangun bertahap pada Sprint 1–6 (lihat [`docs/scrum/`](docs/scrum/README.md)).

## Prasyarat (Windows)

1. **Python 3.11 64-bit**

   ```powershell
   winget install --id Python.Python.3.11 --exact --scope user
   py -0p   # pastikan 3.11 terdaftar
   ```

2. **Tesseract OCR** (dipakai hanya saat membangun knowledge base dari halaman PDF hasil scan)

   ```powershell
   winget install --id UB-Mannheim.TesseractOCR --exact
   ```

   Installer bawaan hanya berisi bahasa Inggris. Tambahkan bahasa Indonesia: unduh [`ind.traineddata`](https://github.com/tesseract-ocr/tessdata/raw/main/ind.traineddata) lalu salin ke `C:\Program Files\Tesseract-OCR\tessdata\` (memerlukan izin administrator). Periksa hasilnya:

   ```powershell
   & "C:\Program Files\Tesseract-OCR\tesseract.exe" --list-langs   # harus memuat eng dan ind
   ```

   Paket Python `pytesseract` **tidak** memasang executable ini. Jika `tesseract` tidak ada di PATH, isi `TESSERACT_CMD` di `.env`.

## Instalasi

```powershell
git clone https://github.com/denisyah1/pekael-chatbot.git
cd pekael-chatbot
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt -e .
```

- `requirements.txt`: dependency runtime yang dipin.
- `requirements-dev.txt`: runtime + pytest.
- `requirements-eval.txt`: runtime + Ragas/OpenAI, khusus skrip evaluasi (tidak diperlukan chatbot maupun deployment):
  `pip install -r requirements-eval.txt`
- `requirements-lock.txt`: seluruh dependency transitif lingkungan pengembangan (dev + eval) hasil `pip freeze`, untuk reproduksi persis:
  `pip install -r requirements-lock.txt -e .`

**FAISS:** `faiss-cpu` terpasang langsung dari pip pada Windows 11 + Python 3.11. Conda/Miniforge hanya diperlukan bila instalasi pip gagal di mesin lain.

## Konfigurasi

```powershell
Copy-Item .env.example .env
```

Isi `.env` dengan nilai asli. File ini di-ignore oleh Git dan **tidak boleh** di-commit.

| Variabel | Keterangan |
|---|---|
| `GEMINI_API_KEY` | Wajib untuk menjawab pertanyaan |
| `ADMIN_USERNAME`, `ADMIN_PASSWORD` | Satu akun admin; login admin nonaktif bila kosong |
| `OPENAI_API_KEY` | Hanya untuk skrip evaluasi Ragas, tidak dibutuhkan chatbot |
| `TESSERACT_CMD` | Contoh: `C:\Program Files\Tesseract-OCR\tesseract.exe` |
| `CHUNK_SIZE`, `CHUNK_OVERLAP`, `RETRIEVAL_K`, `RETRIEVAL_MAX_L2_DISTANCE` | Parameter eksperimen; perubahan dicatat di [`docs/experiment_log.md`](docs/experiment_log.md) |

Nilai kosong atau yang masih berawalan `replace_with_` dianggap belum diisi. Pada hosting, isi variabel yang sama melalui secrets manager platform.

## Perlindungan Secret

Aktifkan hook pre-commit sekali setiap clone:

```powershell
git config core.hooksPath .githooks
```

Hook menjalankan `scripts/check_secrets.py` dan memblokir commit yang memuat file `.env` atau pola API key/password. Pemindaian manual seluruh repo:

```powershell
.\.venv\Scripts\python.exe scripts\check_secrets.py --all
```

Jika sebuah key pernah ter-commit atau terkirim ke tempat lain, anggap sudah bocor: revoke dan buat key baru.

## Pengujian

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Test rutin tidak memanggil API eksternal (memakai embedding palsu/mock). Test yang ditandai `live` dilewati secara default.

Uji model Gemini dengan API sungguhan dijalankan manual (3 panggilan kecil, tanpa retry):

```powershell
.\.venv\Scripts\python.exe scripts\smoke_test_models.py
```

Uji ketiga metrik Ragas (memakai kredit OpenAI API, satu sampel fiktif):

```powershell
.\.venv\Scripts\python.exe scripts\smoke_test_ragas.py
```

Hasil smoke test dicatat di [`docs/technical/smoke_tests.md`](docs/technical/smoke_tests.md).

## Struktur

```text
app.py                  # UI Streamlit (Sprint 4)
src/pekael/
  config/               # AppConfig, AppConfigurator, logging
  core/                 # ChatbotManager, Chain, prompts, schemas
  models/               # GeminiModel
  loaders/              # BaseLoader, PDFLoader, DocumentLoaderFactory
  splitters/            # BaseSplitter, RecursiveCharacterSplitter, DocumentSplitterFactory
  vectorstores/         # BaseVectorStore, FaissVectorStore, VectorStoreFactory
  services/             # OCR, admin auth, pengelolaan sumber
  evaluation/           # dataset dan evaluator Ragas
scripts/                # inspeksi PDF, build knowledge base, smoke test, evaluasi, cek secret
data/                   # sumber, hasil ekstraksi, indeks (tidak di-commit)
tests/                  # unit, integration, fixtures
docs/                   # dokumentasi Scrum, decision log, experiment log
```

## Dokumen Acuan

- [`project_spec.md`](project_spec.md): spesifikasi proyek
- [`implementation_plan.md`](implementation_plan.md): rencana implementasi
- [`docs/scrum/`](docs/scrum/README.md): Product Backlog, sprint, review, retrospective, lembar validasi
- [`docs/decision_log.md`](docs/decision_log.md): keputusan teknis
