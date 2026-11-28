# Uji Coba Ragas (EXP-012) — Rincian Teknis

> Ringkasan berbahasa sederhana: [`docs/scrum/sprint-05/uji_coba_ragas.md`](../scrum/sprint-05/uji_coba_ragas.md)

## 1. Konfigurasi

| Bagian | Nilai |
|---|---|
| Dataset | `data/evaluation/ground_truth.jsonl` v2, scope `uji36` (id 1–30, E1–E6) |
| Indeks Pekael | `20261124T053813125686-565a9929` (Buku Pedoman + dokumen tambahan, 61 potongan) |
| Model jawaban | `gemini-3.5-flash-lite`, `k=4`, ambang `RETRIEVAL_MAX_L2_DISTANCE=0.64`, chunk 1000/150, embedding `gemini-embedding-001` 768 dimensi |
| Evaluator LLM | `openai/gpt-oss-120b` lewat Groq (`https://api.groq.com/openai/v1`), `llm_factory(provider="openai", max_tokens=4096)`, klien `AsyncOpenAI(max_retries=8)` |
| Embedding Answer Relevancy | `ragas.embeddings.GoogleEmbeddings`, `gemini-embedding-001` (dimensi bawaan 3072, terpisah dari indeks) |
| Answer Relevancy `strictness` | 3 (bawaan) |
| Paket | ragas 0.4.3, openai 3.3.0, langchain-core 1.7.0, langchain-google-genai 4.4.2, google-genai 2.33.0, faiss-cpu 1.15.1 |
| Batas Groq (header respons) | `x-ratelimit-limit-requests: 1000` (per hari), `x-ratelimit-limit-tokens: 8000` (per menit). Batas harian token 200000 diketahui dari pesan 429 |

## 2. Kode

- `src/pekael/evaluation/dataset.py`: `GroundTruthEntry`, `load_dataset()` (validasi id unik dan field wajib), `select(scope, ids)` dengan scope `uji36`, `pkl` (38), `all` (44).
- `src/pekael/evaluation/ragas_evaluator.py`: `RagasEvaluator` (impor Ragas, openai, google-genai di dalam konstruktor, FR-11), `_Recorder` membungkus `llm.agenerate`, `embeddings.aembed_text`, `embeddings.aembed_texts` untuk mencatat keluaran terstruktur dan vektor. `explain_faithfulness`, `explain_answer_relevancy` (cosine dihitung ulang dari vektor yang tercatat), `explain_context_recall`.
- `scripts/run_ragas_evaluation.py`: menjawab lewat `manager.chain.invoke(ChainState(...))` (tanpa cache jawaban), menyimpan `retrieved_contexts` = `page_content` keempat potongan, lalu menilai. Baris ditulis per pertanyaan ke `rows.jsonl`. `--resume` melewati baris lengkap dan menilai ulang baris gagal dengan jawaban tersimpan. Berhenti bila pesan error memuat `tokens per day`. Keluaran: `rows.jsonl`, `summary.json`, `scores.csv` di `data/evaluation/results/<experiment>/` (di-ignore Git).
- Hanya kategori `pkl` yang dinilai, `pkl_redirect` dan `non_pkl` diperiksa dari status (D-57).

## 3. Alur tiap metrik (Ragas 0.4.3, `ragas.metrics.collections`)

| Metrik | Masukan | Panggilan LLM | Rumus |
|---|---|---|---|
| Faithfulness | `user_input`, `response`, `retrieved_contexts` | `StatementGeneratorPrompt` → `StatementGeneratorOutput.statements`, lalu `NLIStatementPrompt` (konteks digabung `\n`) → `NLIStatementOutput.statements[].verdict` (0/1) dan `reason` | jumlah `verdict=1` ÷ jumlah pernyataan, NaN bila tidak ada pernyataan |
| Answer Relevancy | `user_input`, `response` | `AnswerRelevancePrompt` 3 kali (`strictness`) → `question`, `noncommittal` | rerata cosine(embedding pertanyaan buatan, embedding pertanyaan asli) × (0 bila semua `noncommittal=1`, selain itu 1) |
| Context Recall | `user_input`, `retrieved_contexts`, `reference` | `ContextRecallPrompt` → `ContextRecallOutput.classifications[].attributed` (0/1) dan `reason` | jumlah `attributed=1` ÷ jumlah pernyataan jawaban acuan |

Panggilan per pertanyaan: Groq 6 kali, embedding Gemini 1 kali untuk pertanyaan asli dan 1 kali (batch) untuk 3 pertanyaan buatan. Prompt Ragas berbahasa Inggris, isi pernyataan mengikuti bahasa jawaban.

## 4. Perintah dan hasil

**Uji integrasi (`EXP-012-probe`)**
- `run_ragas_evaluation.py --experiment EXP-012-probe --ids 29 --pause 0` → Faithfulness gagal `IncompleteOutputException: The output is incomplete due to a max_tokens length limit`, Answer Relevancy 0,901, Context Recall 1,000. Penyebab: `max_tokens` bawaan `InstructorModelArgs` 1024, sedangkan `gpt-oss-120b` memakai token untuk penalaran. Diubah ke 4096 (D-58).
- Ulang `--ids 29,11 --pause 15` → no. 11: 1,000 / 0,903 / 1,000, no. 29: 0,750 / 0,935 / 1,000.

**Uji coba (`EXP-012`)**
- `run_ragas_evaluation.py --experiment EXP-012 --scope uji36 --pause 20`, exit 0.
- No. 1–18 lengkap. Mulai no. 19: `429 ... tokens per day (TPD): Limit 200000, Used 197183, Requested 4041`. Ketiga metrik no. 19–E6 gagal (sebelum perbaikan berhenti otomatis), jawaban Pekael tetap tersimpan. Pemakaian sekitar 197 ribu token untuk 21 pertanyaan (18 + 3 percobaan integrasi), sekitar 9.400 token per pertanyaan.
- Semua 36 jawaban berstatus `answered`, `answer_seconds` median 1,79 s.

| id | Faithfulness | Answer Relevancy | Context Recall | Konteks yang terambil |
|---|---|---|---|---|
| 1 | 1,000 | 0,885 | 1,000 | |
| 2 | 1,000 | 0,986 | 0,500 | Pedoman 13, 14, KB 4, KB 3 |
| 3 | 0,800 | 0,877 | 1,000 | Pedoman 5, 5, 23, 7 |
| 4 | 1,000 | 0,809 | 1,000 | |
| 5 | 0,800 | 0,980 | 1,000 | KB 3, Pedoman 14, 13, 7 |
| 6 | 1,000 | 0,907 | 1,000 | |
| 7 | 1,000 | 0,888 | 1,000 | |
| 8 | 1,000 | 0,992 | 1,000 | |
| 9 | 1,000 | 0,848 | 1,000 | |
| 10 | 0,875 | 0,883 | 1,000 | KB 2, KB 2, Pedoman 9, 10 |
| 11 | 1,000 | 0,884 | 1,000 | |
| 12 | 1,000 | 0,997 | 1,000 | |
| 13 | 1,000 | 0,835 | 1,000 | |
| 14 | 0,500 | 0,897 | 1,000 | Pedoman 11, KB 1, KB 2, KB 1 |
| 15 | 0,333 | 0,854 | 1,000 | KB 5, Pedoman 11, KB 5, KB 4 |
| 16 | 0,900 | 0,964 | 1,000 | KB 5, Pedoman 11, 11, 15 |
| 17 | 1,000 | 0,992 | 1,000 | |
| 18 | 1,000 | 0,833 | 1,000 | |

Rerata 18 pertanyaan: Faithfulness 0,9005 (median 1,0, min 0,3333), Answer Relevancy 0,9061 (median 0,8866, min 0,8091), Context Recall 0,9722 (median 1,0, min 0,5).

## 5. Analisis nilai rendah (spec §10.3 langkah 6)

| id | Metrik | Pernyataan yang tidak didukung | Kelompok penyebab |
|---|---|---|---|
| 3 | Faithfulness 0,8 | "Tujuan PKL penting untuk dipahami sebelum terjun ke lapangan" | Prompt (kalimat pengantar) |
| 5 | Faithfulness 0,8 | "Durasi PKL harus dipenuhi agar kegiatan berjalan lancar" | Prompt (kalimat penutup) |
| 10 | Faithfulness 0,875 | "Mentor mendampingi dan memberi arahan bersama dosen pembimbing" | Generation (tambahan yang tidak tertulis) |
| 14 | Faithfulness 0,5 | "Berikut adalah syarat tambahan", "Informasi tersebut diharapkan membantu persiapan PKL" | Prompt (pengantar dan penutup) |
| 15 | Faithfulness 0,333 | Empat syarat kelulusan dibaca sebagai klaim bahwa mahasiswa telah memenuhinya ("The context lists this as a graduation requirement, not as a confirmed fact about a particular student") | Evaluator (salah tafsir, jawaban sesuai sumber) |
| 16 | Faithfulness 0,9 | "Pengulangan wajib bila mahasiswa melakukan pelanggaran berat" | Generation (kata "berat" tidak ada di sumber) |
| 2 | Context Recall 0,5 | UU No. 20 Tahun 2003 dan Kepmendikbud No. 754/P/2020 (Pedoman hlm. 4–5) tidak terambil | Retrieval |

Answer Relevancy: tebakan pertanyaan kadang identik tiga kali (no. 29 percobaan integrasi) dan kadang berbahasa Inggris (no. 14 tebakan 3: cosine 0,790 dibanding 0,951 untuk tebakan berbahasa Indonesia).

## 6. Jejak lengkap no. 14 (dari `rows.jsonl`)

- `response`: "Tentu, untuk kamu yang mau PKL di luar negeri atau PKL Internasional, ada syarat tambahan yang harus dipenuhi ya. Berikut adalah syarat tambahannya: • Memperoleh izin orang tua jika melaksanakan Praktik Kerja Lapangan (PKL) Internasional. Semoga informasi ini bisa membantu kelancaran persiapan PKL kamu, ya!"
- `retrieved_sources`: Pedoman hlm. 11 (0,4552), KB hlm. 1 (0,4749), KB hlm. 2 (0,5005), KB hlm. 1 (0,5109). `cited_sources`: Pedoman 11, KB 1.
- Faithfulness (5,84 s): 4 pernyataan, `verdict` [1, 0, 1, 0] → 0,5.
- Answer Relevancy (7,50 s): pertanyaan buatan "Apa syarat tambahan untuk melakukan PKL Internasional?" (0,9511) dua kali dan "What additional requirement must be met for an international PKL?" (0,7900), `noncommittal` 0 → (0,9511 + 0,9511 + 0,7900) ÷ 3 = 0,8974.
- Context Recall (18,71 s, termasuk menunggu batas token per menit): 1 pernyataan acuan, `attributed` 1 → 1,0.

## 7. Kuota dan jadwal

- Sekitar 9.400 token per pertanyaan, batas harian 200.000 token → sekitar 21 pertanyaan per 24 jam untuk satu model. Evaluasi 38 pertanyaan (Sprint 6) memerlukan dua hari dengan `--resume`.
- Lanjutan uji coba: `run_ragas_evaluation.py --experiment EXP-012 --scope uji36 --pause 20 --resume` (hanya menilai ulang no. 19–E6, jawaban Pekael tidak diminta ulang).

## 8. Test

- `tests/unit/test_evaluation.py` (7 test, tanpa API): scope `uji36` berisi 36 id, pemuatan dan pemilihan dataset, penolakan id ganda dan baris tidak lengkap, rumus penjelasan ketiga metrik, dan `pekael.ui.student_page` tidak memuat `ragas`, `openai`, atau `pekael.evaluation.ragas_evaluator`.
