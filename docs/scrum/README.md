# Dokumentasi Scrum — Pekael

Folder ini adalah catatan resmi pelaksanaan Scrum untuk penelitian skripsi Pekael. Isinya dipakai sebagai bahan laporan per sprint, lampiran skripsi, dan lembar validasi Product Owner.

## Tim Scrum

| Peran | Nama | Tanggung jawab dalam proyek ini |
|---|---|---|
| Product Owner | Bambang Satrio, S. Pd., M. Kom. | Memvalidasi knowledge base, Sprint Goal, increment, dan dataset ground truth |
| Scrum Master | Dr. Widodo, M. Kom. dan Nur Elah, S. Kom., M.T. | Menjaga jalannya event Scrum dan menghapus hambatan |
| Developer | Deni Merdiansyah | Merencanakan, membangun, menguji, dan mendokumentasikan increment |

## Ritme

- 6 sprint menghasilkan **satu MVP** (spec §12). Sprint 1–3 masing-masing 1 minggu karena pengembangan dimulai lebih lambat dari rencana, Sprint 4–6 masing-masing 2 minggu (D-19).
- **Awal sprint:** Sprint Planning → Lembar Validasi Sprint Report Bagian A ditandatangani PO → sprint dimulai.
- **Selama sprint:** setiap sesi kerja dicatat di `sprint_backlog.md` sprint tersebut (bagian *Log Pengerjaan*).
- **Akhir sprint:** Sprint Review → Lembar Validasi Bagian B (PO) → Sprint Retrospective → Lembar Validasi Bagian C (Scrum Master) → Product Backlog diperbarui.

## Struktur

```text
docs/
├── scrum/
│   ├── README.md                 # file ini: tim, ritme, status sprint
│   ├── product_backlog.md        # Product Backlog + riwayat perubahan
│   ├── setup_phase.md            # catatan fase Setup (sebelum Sprint 1)
│   ├── templates/                # templat yang disalin ke tiap sprint
│   └── sprint-NN/
│       ├── sprint_planning.md       # Lembar Validasi Bagian A (planning + validasi PO)
│       ├── sprint_backlog.md        # task + logbook harian
│       ├── sprint_review.md         # Lembar Validasi Bagian B (review + validasi PO)
│       └── sprint_retrospective.md  # Lembar Validasi Bagian C (retro + konfirmasi Scrum Master)
├── technical/                    # rincian teknis: log perintah, versi, hasil smoke test
│   ├── setup_log.md
│   └── smoke_tests.md
├── decision_log.md               # keputusan teknis (D-xx) dan penyelesaian Open Decision (OD-xx)
└── experiment_log.md             # eksperimen chunking, threshold, model (NFR-06)
```

Dokumen di `docs/scrum/` ditulis dengan bahasa sederhana sebagai bahan laporan. Rincian teknis (perintah, versi paket, keluaran test) ada di `docs/technical/` dan dirujuk lewat tautan.

## Status Sprint

| Sprint | Periode | Sprint Goal | Planning | Review | Retro | Status |
|---|---|---|---|---|---|---|
| Setup | 23 Okt 2026 | Lingkungan dan kerangka kode siap dibangun | — | — | — | Selesai (uji evaluator OpenAI tertunda) |
| 1 | 23–29 Okt 2026 | Persiapan dan validasi knowledge base | ✓ 23 Okt (tanda tangan fisik menyusul) | Draf siap (29 Okt) | Draf siap (29 Okt) | Menunggu hasil review PO |
| 2 | 30 Okt – 6 Nov 2026 | Chunking dan embedding | Disusun 30 Okt | ☐ | ☐ | Berjalan |
| 3 | 6 – 12 Nov 2026 | FAISS dan alur RAG inti | ☐ | ☐ | ☐ | Belum dimulai |
| 4 | 13 – 26 Nov 2026 (rencana) | UI Streamlit dan pengujian internal | ☐ | ☐ | ☐ | Belum dimulai |
| 5 | 27 Nov – 10 Des 2026 (rencana) | Validasi ahli dan revisi | ☐ | ☐ | ☐ | Belum dimulai |
| 6 | 11 – 24 Des 2026 (rencana) | Deployment, Ragas, UAT, analisis | ☐ | ☐ | ☐ | Belum dimulai |

## Aturan Pencatatan

1. Catat fakta yang terjadi: perintah yang dijalankan, hasil test (lulus/gagal beserta jumlahnya), file yang berubah, dan keputusan. Jangan menulis klaim yang belum diuji.
2. Hasil yang gagal tetap dicatat beserta tindak lanjutnya.
3. Setiap perubahan Product Backlog dicatat di bagian *Riwayat Perubahan* `product_backlog.md`.
4. Jangan mencantumkan API key, password, atau data responden.
5. Lembar validasi ditandatangani manual oleh PO, lalu hasil pindaian disimpan di luar repo. Repo hanya mencatat status ✓ dan tanggalnya.
