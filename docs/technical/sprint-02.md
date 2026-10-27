# Log Teknis Sprint 2

> Ringkasan berbahasa sederhana: [`docs/scrum/sprint-02/`](../scrum/sprint-02/sprint_backlog.md)

## Sesi 1 — 30 Oktober 2026

**Pemilihan halaman (S2-T03)**
- `loaders/pdf_loader.py`: `parse_page_ranges("4-16,27-28")` → daftar halaman 1-based (menolak `a-3`, `5-2`, `0-3`, `4-`). `PDFLoader(pages=[...])` hanya memuat halaman terpilih, `DocumentLoadError` bila melebihi jumlah halaman PDF. `total_pages` tetap jumlah halaman PDF.
- `AppConfig.knowledge_base_pages` (`KNOWLEDGE_BASE_PAGES`, divalidasi saat startup). `.env.example` diberi baris kosong dengan keterangan "isi setelah persetujuan PO".
- Bug ditemukan oleh test dan diperbaiki: `"4-"` semula diterima sebagai halaman 4.

**Splitter (S2-T04)**
- `splitters/recursive_character_splitter.py`: membungkus `RecursiveCharacterTextSplitter` (`separators=["\n\n", "\n", ". ", " ", ""]`, `add_start_index=True`). Satu halaman dipotong terpisah (potongan tidak melintasi halaman).
- Metadata tambahan: `chunk_id = <source_hash[:8]>-p<hal:03>-c<urut:02>`, `chunk_index`, `section`. `start_index` dibuang setelah dipakai.
- `section`: judul yang berlaku di awal potongan + semua judul di dalam potongan yang masih diikuti teks, digabung `" / "`. Judul dikenali dengan pola BAB (`BAB [IVXL]+` + baris judul kapital) dan subbab (`^[A-Z]\.\s+[A-Z][^.]{2,80}$`). Bagian terakhir halaman terbawa ke halaman berikutnya. Butir daftar huruf kecil (`a.`, `b.`) tidak dianggap judul.
- Iterasi: versi pertama memberi label hanya judul terakhir sehingga `p014-c01` (isi mayoritas subbab B) berlabel "C. Sanksi", dan `p016` mewarisi "C. Sanksi" dari BAB II. Diperbaiki dengan label gabungan dan deteksi BAB.

**Laporan potongan (S2-T05)** — `scripts/inspect_chunks.py data\source\Pedoman-PKL-2025.pdf --pages 4-16 --configs 500:50,800:100,1000:150,1500:200`
- 13 halaman dimuat, koreksi manual aktif pada hal. 4, 5, 6, 8, 10, 11, 13, 14, 16.

| size:overlap | chunks | min | mean | max | per hal. | tanpa bagian | duplikat |
|---|---|---|---|---|---|---|---|
| 500:50 | 49 | 36 | 340 | 498 | 3,8 | 0 | 0 |
| 800:100 | 33 | 36 | 519 | 790 | 2,5 | 0 | 0 |
| 1000:150 | 26 | 36 | 668 | 995 | 2,0 | 0 | 0 |
| 1500:200 | 18 | 232 | 953 | 1444 | 1,4 | 0 | 0 |

- Potongan 36 karakter = `565a9929-p004-c01` "BAB I / PENDAHULUAN / A. Latar Belakang" (hanya judul). Dicatat untuk EXP-002.
- Keluaran: `data/processed/Pedoman-PKL-2025/chunks_<size>_<overlap>.jsonl` (di-ignore git).

**Test**: `pytest` → **130 lulus, 0 gagal** (baru: `test_splitter.py` 13 test, pemilihan halaman 11 test di `test_pdf_loader.py`, 1 test di `test_config.py`).
