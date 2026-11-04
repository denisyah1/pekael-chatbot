# Log Teknis Sprint 4

> Ringkasan berbahasa sederhana: [`docs/scrum/sprint-04/`](../scrum/sprint-04/sprint_backlog.md)

## Sesi 1 — 13 November 2026

**Penutupan Sprint 3**: S3-T01 Done (verifikasi Developer), review dan retrospective Sprint 3 ditandai diterima, PBI-01, PBI-04, PBI-05 `Diterima PO`.

**Halaman mahasiswa (S4-T02, S4-T03)**
- `app.py` (entry point, spec §5.4) memanggil `pekael.ui.student_page.main()`.
- `src/pekael/ui/student_page.py`:
  - `get_config()` dan `get_manager()` memakai `st.cache_resource`, sehingga satu `ChatbotManager` dan satu indeks FAISS dipakai bersama oleh semua sesi pada satu proses server.
  - `load_manager()` → `(manager, None)`, atau pesan `NOT_CONFIGURED` (`ConfigError`/`EmbeddingError`/`LLMError` saat perakitan, misalnya `GEMINI_API_KEY` kosong), atau `NOT_READY` (`IndexNotReadyError`). Indeks dimuat sekali (`is_ready`).
  - `st.form(clear_on_submit=True)`: `st.text_area` (`max_chars=QUESTION_MAX_CHARS`) dan tombol "Kirim". `st.spinner` selama `generate_response`.
  - Riwayat `st.session_state["history"]` berisi `Exchange(question, response)`, terbaru di atas, hanya untuk tampilan (FR-10). `INVALID_INPUT` tidak disimpan.
  - Status: `answered` → jawaban + `st.caption("Sumber: <dokumen>, halaman PDF ...")` + `st.expander` cuplikan per potongan. `out_of_scope` → `st.info`. `unavailable`/`error` → `st.warning`.
- `.streamlit/config.toml`: tema terang, `primaryColor="#1F6F43"`, `toolbarMode="minimal"`, `gatherUsageStats=false`. `.streamlit/secrets.toml` tetap di-ignore.
- README: bagian "Menjalankan Pekael".

**Uji**
- `tests/unit/test_student_page.py` (9 test, `streamlit.testing.v1.AppTest` dengan manager tiruan): tampilan awal, jawaban + sumber + kutipan, penolakan, gangguan layanan, pertanyaan kosong, urutan riwayat dan hapus riwayat, knowledge base belum ada, pengaturan belum lengkap.
- `streamlit run app.py --server.headless true --server.port 8599` → `/_stcore/health` = `ok`, halaman HTTP 200.
- AppTest dengan manager asli (indeks `20261104T043244948591-565a9929`): "Kalau nilai saya 74, apakah saya lulus PKL?" → `answered`, 3 rujukan (hal. 16, 11, 11), 19,70 s (pertanyaan pertama setelah start). "Bagaimana cara membuat nasi goreng?" → `out_of_scope` oleh ambang (jarak 0,831), 0,47 s. Tidak ada exception.
- `pytest` → **233 lulus, 0 gagal**.
