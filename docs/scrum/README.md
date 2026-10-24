# Dokumentasi Scrum — Pekael

Folder ini adalah catatan resmi pelaksanaan Scrum untuk penelitian skripsi Pekael. Isinya dipakai sebagai bahan laporan per sprint, lampiran skripsi, dan lembar validasi Product Owner.

## Tim Scrum

| Peran | Nama | Tanggung jawab dalam proyek ini |
|---|---|---|
| Product Owner | Bambang Satrio, S. Pd., M. Kom. | Memvalidasi knowledge base, Sprint Goal, increment, dan dataset ground truth |
| Scrum Master | Dr. Widodo, M. Kom. dan Nur Elah, S. Pd., M. Kom. | Menjaga jalannya event Scrum dan menghapus hambatan |
| Developer | Deni Merdiansyah | Merencanakan, membangun, menguji, dan mendokumentasikan increment |

## Ritme

- 6 sprint × 2 minggu = 12 minggu, menghasilkan **satu MVP** (spec §12).
- **Awal sprint:** Sprint Planning → Lembar Validasi Planning ditandatangani PO → sprint dimulai.
- **Selama sprint:** setiap sesi kerja dicatat di `sprint_backlog.md` sprint tersebut (bagian *Log Pengerjaan*).
- **Akhir sprint:** Sprint Review → Lembar Validasi Review → Sprint Retrospective → Product Backlog diperbarui.

## Struktur

```text
docs/
├── scrum/
│   ├── README.md                 # file ini: tim, ritme, status sprint
│   ├── product_backlog.md        # Product Backlog + riwayat perubahan
│   ├── setup_phase.md            # catatan fase Setup (sebelum Sprint 1)
│   ├── templates/                # templat yang disalin ke tiap sprint
│   └── sprint-NN/
│       ├── sprint_planning.md
│       ├── validasi_planning.md
│       ├── sprint_backlog.md     # task + log pengerjaan harian
│       ├── sprint_review.md
│       ├── validasi_review.md
│       └── sprint_retrospective.md
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
| Setup | 2026-10-25 | Lingkungan dan kerangka kode siap dibangun | — | — | — | Selesai (uji evaluator OpenAI tertunda) |
| 1 | _[tgl]_ | Persiapan dan validasi knowledge base | ☐ | ☐ | ☐ | Belum dimulai |
| 2 | _[tgl]_ | Chunking dan embedding | ☐ | ☐ | ☐ | Belum dimulai |
| 3 | _[tgl]_ | FAISS dan alur RAG inti | ☐ | ☐ | ☐ | Belum dimulai |
| 4 | _[tgl]_ | UI Streamlit dan pengujian internal | ☐ | ☐ | ☐ | Belum dimulai |
| 5 | _[tgl]_ | Validasi ahli dan revisi | ☐ | ☐ | ☐ | Belum dimulai |
| 6 | _[tgl]_ | Deployment, Ragas, UAT, analisis | ☐ | ☐ | ☐ | Belum dimulai |

## Aturan Pencatatan

1. Catat fakta yang terjadi: perintah yang dijalankan, hasil test (lulus/gagal beserta jumlahnya), file yang berubah, dan keputusan. Jangan menulis klaim yang belum diuji.
2. Hasil yang gagal tetap dicatat beserta tindak lanjutnya.
3. Setiap perubahan Product Backlog dicatat di bagian *Riwayat Perubahan* `product_backlog.md`.
4. Jangan mencantumkan API key, password, atau data responden.
5. Lembar validasi ditandatangani manual oleh PO, lalu hasil pindaian disimpan di luar repo. Repo hanya mencatat status ✓ dan tanggalnya.
