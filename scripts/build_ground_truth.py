"""Ground truth dataset for Ragas and the repeated tests (Sprint 5, spec §10.2, SUP-01).

This file is the single source of the 40 entries: 36 PKL questions (the test questions of
Sprint 4) with reference answers written from the approved knowledge base, and 4 questions
outside PKL with the expected behaviour. It writes

- ``data/evaluation/ground_truth.jsonl``: the dataset with reference contexts (full text of the
  source pages) and source pages, read by the evaluation scripts (not committed, NFR-07),
- ``docs/scrum/sprint-05/dataset_ground_truth.md``: the validation sheet for the Product Owner,
  without source pages.

Corrections from the Product Owner are made here, then the script is run again so the
dataset and the sheet stay identical. No API calls. Usage from the project root:

    .venv\\Scripts\\python.exe scripts\\build_ground_truth.py
"""

import json
import sys
from pathlib import Path

VERSION = "v1"
DRAFTED = "22 November 2026"
HANDBOOK = "Pedoman-PKL-2025.pdf"
EXTRA = "Knowledge_Base_PKL_PTIK_UNJ-2.pdf"
HANDBOOK_PAGES = Path("data/processed/Pedoman-PKL-2025")
EXTRA_PDF = Path("data/source") / EXTRA
DATASET = Path("data/evaluation/ground_truth.jsonl")
SHEET = Path("docs/scrum/sprint-05/dataset_ground_truth.md")


def P(*pages: int) -> list[tuple[str, int]]:
    return [(HANDBOOK, p) for p in pages]


def K(*pages: int) -> list[tuple[str, int]]:
    return [(EXTRA, p) for p in pages]


# (id, topic, question type, question, reference answer, sources, note for the Product Owner)
PKL = [
    ("1", "Pengertian PKL", "Langsung", "Apa yang dimaksud dengan Praktik Kerja Lapangan?",
     "Praktik Kerja Lapangan (PKL) adalah kegiatan kurikuler yang wajib dilakukan mahasiswa sebagai salah satu syarat menyelesaikan studi. "
     "PKL dilaksanakan di dalam atau di luar kampus sebagai bagian dari pengembangan diri pada dunia kerja, di tempat PKL seperti instansi pemerintah atau swasta, "
     "dunia usaha dan dunia industri (DUDI), lembaga swadaya masyarakat, lembaga diklat, sekolah, dan koperasi, baik di dalam maupun di luar negeri, "
     "untuk menerapkan ilmu pengetahuan dan keterampilan mahasiswa sesuai bidang keilmuannya.",
     P(5), None),
    ("2", "Dasar hukum PKL", "Daftar", "PKL di UNJ mengacu pada peraturan apa saja?",
     "PKL mengacu pada: (1) Undang-Undang Nomor 20 Tahun 2003 tentang Sistem Pendidikan Nasional, "
     "(2) Permendikbud Nomor 3 Tahun 2020 tentang Standar Nasional Pendidikan Tinggi, yang menyebut pengalaman kerja sebagai bagian dari standar kompetensi lulusan dan menjadi dasar bobot 170 menit per minggu per SKS (pasal 19 ayat 4), dan "
     "(3) Kepmendikbud Nomor 754/P/2020 tentang Indikator Kinerja Utama, khususnya IKU 2 bahwa mahasiswa mendapatkan pengalaman di luar kampus. "
     "Jumlah SKS PKL mengikuti aturan UNJ.",
     P(4, 5, 13), None),
    ("3", "Tujuan PKL", "Daftar", "Apa tujuan dilaksanakannya PKL?",
     "Tujuan PKL adalah: (1) menyiapkan mahasiswa agar memiliki pengalaman faktual dengan menerapkan ilmu dan keterampilan dari perkuliahan di industri atau lembaga, "
     "(2) memberi kesempatan mahasiswa menerapkan kemampuan profesional atau keahliannya secara utuh dan terpadu dalam situasi nyata, "
     "(3) memberi pemahaman tentang prosedur kerja dan peraturan teknis di dunia kerja, dan "
     "(4) mengembangkan diri mahasiswa sebagai tenaga profesional yang disiplin dan bertanggung jawab dalam melaksanakan tugas.",
     P(5, 6), None),
    ("4", "Manfaat PKL", "Daftar, beberapa bagian", "PKL bermanfaat apa untuk mahasiswa? Untuk mitra?",
     "Bagi mahasiswa, PKL bermanfaat untuk mengimplementasikan teori, mengembangkan kemampuan dan keterampilan di bidang terkait, membangun etos kerja dan rasa tanggung jawab, "
     "mempertajam analisis kebutuhan pekerjaan, memberi gambaran nyata dunia kerja, menambah wawasan agar menjadi tenaga kerja yang kompeten, "
     "melatih berpikir kritis, kreatif, dan bertanggung jawab, serta melatih karakter positif, berintegritas, dan inovatif. "
     "Bagi mitra, PKL bermanfaat untuk meningkatkan kerja sama dengan perguruan tinggi dalam memperoleh tenaga kerja yang kompeten, "
     "menjadi jembatan kerja sama lebih lanjut di bidang akademis maupun nonakademis, dan mendapatkan bantuan tenaga profesional dalam penyelesaian pekerjaan.",
     P(6, 7), None),
    ("5", "Lama pelaksanaan", "Angka", "Berapa lama PKL harus dilaksanakan?",
     "PKL dilaksanakan minimal 4 bulan atau satu semester. Mahasiswa dinyatakan menyelesaikan PKL bila telah memenuhi waktu yang ditentukan program studi dan mitra PKL.",
     P(7, 11, 14) + K(3), None),
    ("6", "Jenis tempat PKL", "Daftar", "Di mana saja PKL boleh dilaksanakan?",
     "Tempat PKL bersumber dari mitra universitas, fakultas, atau program studi, yaitu instansi pemerintah, BUMN atau BUMD, dunia industri, lembaga keuangan, desa wisata, galeri seni, "
     "lembaga pendidikan, lembaga diklat, LSM atau NGO, dan tempat lain yang dianggap relevan. PKL boleh di dalam maupun di luar negeri. "
     "Mahasiswa juga dapat mengusulkan tempat PKL sendiri sesuai ketentuan program studi.",
     P(5, 7) + K(2), None),
    ("7", "Mengusulkan tempat sendiri", "Persyaratan, parafrasa", "Bolehkah saya mencari tempat PKL sendiri? Apa syaratnya?",
     "Boleh. Tempat PKL yang diusulkan mahasiswa harus bersedia membuat MoU dengan universitas atau MoA dengan fakultas atau program studi, dan/atau memenuhi kriteria program studi, "
     "yaitu bukan home industry dan memiliki website resmi organisasi atau perusahaan.",
     P(7) + K(2), None),
    ("8", "Penetapan tempat dan dosen pembimbing", "Langsung", "Siapa yang menetapkan tempat dan dosen pembimbing PKL?",
     "Program studi menentukan kelompok, lembaga atau tempat PKL, dan dosen pembimbing PKL, dengan kemungkinan mahasiswa mengusulkan tempat yang relevan. "
     "Koordinator PKL Prodi menetapkan syarat, waktu, dan tempat pelaksanaan PKL serta menugaskan mahasiswa pada tempat yang ditetapkan. "
     "Di PTIK, setelah mahasiswa mendaftar, prodi menetapkan dosen pembimbingnya.",
     P(8, 13) + K(2), None),
    ("9", "Tugas dosen pembimbing", "Daftar", "Apa saja tugas dosen pembimbing PKL?",
     "Dosen pembimbing bertugas: (1) menghadiri pembekalan PKL yang diselenggarakan Pusat PKM/PPL/PKL/Magang UNJ, fakultas, atau prodi, "
     "(2) mengantarkan mahasiswa PKL ke instansi yang telah ditetapkan, (3) memberikan umpan balik berdasarkan hasil refleksi mahasiswa, dan "
     "(4) menilai presentasi, laporan akhir PKL, dan berita acara PKL.",
     P(8, 9), None),
    ("10", "Tugas pembimbing lapangan (mentor)", "Daftar", "Apa peran mentor di tempat PKL?",
     "Pembimbing lapangan (mentor) bertugas: (1) membimbing mahasiswa menyusun program PKL, (2) memberikan bimbingan dan bantuan selama PKL berlangsung, "
     "(3) memonitor kehadiran mahasiswa, (4) menandatangani laporan kegiatan mahasiswa, dan (5) memberikan nilai sesuai format yang telah disediakan.",
     P(9), None),
    ("11", "Kewajiban mahasiswa peserta PKL", "Daftar", "Apa saja kewajiban saya selama PKL?",
     "Mahasiswa peserta PKL wajib: mengikuti pembekalan dan pembukaan, memastikan kesiapan diri, berkoordinasi secara berkala dengan dosen pembimbing, "
     "menyusun program kerja bersama pembimbing dan melaksanakannya, mengisi daftar hadir, menjalin kerja sama yang baik dengan pembimbing, staf instansi, dan sesama peserta, "
     "menjaga disiplin waktu, pakaian, dan sopan santun, mengikuti peraturan instansi, menerima arahan dan teguran pembimbing, melaksanakan PKL sesuai waktu yang ditentukan, "
     "meminta izin kepada dosen pembimbing lapangan dan mentor bila berhalangan hadir, mendokumentasikan setiap kegiatan, membuat laporan akhir, mempresentasikannya kepada dosen pembimbing, "
     "dan menyerahkan laporan kepada dosen pembimbing, program studi, dan instansi.",
     P(9, 10), None),
    ("12", "Syarat minimal SKS", "Angka, persyaratan", "Berapa SKS minimal untuk bisa ikut PKL?",
     "Mahasiswa dapat menjadi peserta PKL bila telah memenuhi minimal 100 SKS. Bila di tengah pelaksanaan ternyata belum memenuhi 100 SKS, prodi berhak menarik mahasiswa tersebut dari PKL.",
     P(10) + K(1), None),
    ("13", "Mata kuliah prasyarat", "Persyaratan", "Mata kuliah apa saja yang harus sudah ditempuh sebelum PKL?",
     "Mata kuliah prasyarat PKL adalah Mata Kuliah Umum (MKU), Mata Kuliah Dasar Kependidikan (MKDK) sesuai prodi masing-masing, dan Mata Kuliah Program Studi sesuai ketentuan program studi.",
     P(10) + K(1), None),
    ("14", "PKL internasional", "Persyaratan", "Apa syarat tambahan kalau PKL di luar negeri?",
     "Mahasiswa yang melaksanakan PKL internasional (di luar negeri) harus memperoleh izin orang tua, selain memenuhi persyaratan peserta PKL lainnya.",
     P(11) + K(1), None),
    ("15", "Syarat kelulusan PKL", "Persyaratan, daftar", "Kapan saya dinyatakan lulus PKL?",
     "Mahasiswa dinyatakan menyelesaikan PKL bila: (1) telah memenuhi waktu yang ditentukan program studi dan mitra PKL, "
     "(2) telah membuat laporan akhir PKL untuk diserahkan kepada pembimbing lapangan, program studi, atau Pusat PKM/PKL, "
     "(3) telah mempresentasikan laporan kepada dosen pembimbing, dan (4) telah memperoleh nilai minimal B+ dari pembimbing lapangan dan dosen pembimbing.",
     P(11) + K(5), None),
    ("16", "Kondisi harus mengulang", "Daftar", "Dalam kondisi apa mahasiswa harus mengulang PKL?",
     "Mahasiswa harus mengulang PKL bila: (1) melanggar norma dan etika di tempat PKL sehingga mencoreng nama baik UNJ, "
     "(2) tidak mematuhi aturan Buku Pedoman, tidak mengikuti seminar laporan, atau terlambat menyerahkan laporan PKL, atau "
     "(3) tidak lulus atau mendapat nilai kurang dari B+.",
     P(11) + K(5), None),
    ("17", "Tata tertib", "Daftar", "Apa aturan berpakaian dan kehadiran selama PKL?",
     "Peserta PKL wajib disiplin waktu (datang dan pulang sesuai waktu yang ditetapkan), berpakaian dan berpenampilan rapi, sopan, dan mengikuti ketentuan tempat PKL, "
     "dan bagi laki-laki rambut tidak gondrong. Mahasiswa mengisi daftar hadir selama PKL, dan bila berhalangan hadir (izin atau sakit) harus melampirkan surat izin atau surat sakit kepada dosen pembimbing lapangan.",
     P(9, 11) + K(3), None),
    ("18", "Izin tidak hadir", "Prosedur, beberapa bagian", "Bagaimana kalau saya sakit saat PKL?",
     "Mahasiswa yang sakit meminta izin kepada dosen pembimbing lapangan dan pembimbing lapangan (mentor) sesuai prosedur yang ditetapkan, "
     "dan melampirkan surat sakit kepada dosen pembimbing lapangan.",
     P(10, 11) + K(3), None),
    ("19", "Alur pengajuan PKL", "Prosedur bertahap", "Bagaimana langkah-langkah mengajukan PKL?",
     "Menurut Buku Pedoman: (1) memenuhi persyaratan umum, (2) mengajukan permohonan PKL ke program studi, (3) mendaftar online di SIAKAD, "
     "(4) program studi menentukan kelompok, tempat PKL, dan dosen pembimbing, (5) menyusun proposal dan CV, (6) membuat surat permohonan PKL, "
     "(7) proaktif menindaklanjuti ke tempat PKL, dan (8) melaksanakan PKL setelah ada jawaban dari tempat PKL. "
     "Pada praktiknya di PTIK, mahasiswa lebih dulu mencari instansi sendiri, lalu setelah mendaftar ditetapkan dosen pembimbingnya dan mengisi Google Form dari Admin Prodi.",
     P(13) + K(1, 2), "Bagian praktik di PTIK berasal dari dokumen knowledge base tambahan."),
    ("20", "Pendaftaran PKL", "Langsung", "Di mana saya mendaftar PKL?",
     "Pendaftaran PKL dilakukan secara online di SIAKAD setelah mengajukan permohonan ke program studi. Di PTIK, PKL juga didaftarkan di KRS, lalu mahasiswa mengisi Google Form yang tautannya diberikan Admin Prodi.",
     P(13) + K(1, 2), "Bagian KRS dan Google Form berasal dari dokumen knowledge base tambahan."),
    ("21", "Bobot dan jumlah SKS PKL", "Angka", "PKL berapa SKS dan berapa menit per minggu?",
     "PKL berbobot 6 SKS sesuai aturan UNJ, atau diatur program studi sesuai kurikulumnya. Bobot per SKS adalah 170 menit per minggu per semester sesuai Permendikbud Nomor 3 Tahun 2020, "
     "sehingga 6 SKS setara 1.020 menit atau 17 jam per minggu.",
     P(13, 14) + K(3), "Perhitungan 1.020 menit (17 jam) per minggu berasal dari dokumen knowledge base tambahan."),
    ("22", "Alur pelaksanaan PKL", "Prosedur bertahap", "Apa saja tahapan setelah saya diterima di tempat PKL?",
     "Setelah permohonan disetujui: (1) program studi memberikan surat pengantar PKL dan Panduan PKL ke instansi, (2) program studi memberikan pembekalan sebelum PKL dimulai, "
     "(3) mahasiswa melaksanakan PKL minimal 4 bulan atau satu semester, (4) mahasiswa menyerahkan catatan kegiatan mingguan dan berkonsultasi kepada dosen pembimbing lapangan setiap minggu, dan "
     "(5) setelah PKL, mahasiswa membuat laporan hasil PKL yang dilampiri dokumentasi.",
     P(14) + K(1), None),
    ("23", "Pembekalan PKL", "Langsung, beberapa bagian", "Apakah ada pembekalan sebelum PKL? Siapa yang menyelenggarakan?",
     "Ada. Pembekalan diberikan sebelum PKL dimulai. Pembekalan diselenggarakan oleh Pusat PKM/PPL/PKL/Magang UNJ, fakultas, atau program studi, "
     "dan kegiatan pembekalan mahasiswa dikoordinasikan oleh Koordinator PKL Prodi. Mahasiswa wajib mengikuti pembekalan dan pembukaan sesuai waktu yang ditentukan.",
     P(8, 9, 14), None),
    ("24", "Penyerahan laporan", "Daftar", "Kepada siapa laporan PKL diserahkan?",
     "Laporan hasil PKL diserahkan kepada dosen pembimbing, program studi, dan instansi tempat PKL. Syarat kelulusan juga menyebut laporan akhir diserahkan kepada pembimbing lapangan, "
     "program studi, atau Pusat PKM/PKL, dan laporan dipresentasikan kepada dosen pembimbing.",
     P(10, 11) + K(3), None),
    ("25", "Sanksi mahasiswa", "Persyaratan", "Apa sanksinya jika saya tidak menyelesaikan PKL tepat waktu?",
     "Mahasiswa dinyatakan tidak lulus mata kuliah PKL bila tidak mengikuti kegiatan PKL hingga batas waktu yang ditentukan, tidak membuat laporan akhir, dan/atau tidak mengikuti ujian atau seminar hasil PKL. "
     "Mahasiswa yang terlambat menyerahkan laporan PKL harus mengulang PKL. Teguran dari dosen pembimbing lapangan diberikan bila mahasiswa tidak memenuhi petunjuk yang ditetapkan.",
     P(11, 14, 15) + K(5), None),
    ("26", "Sanksi dosen pembimbing", "Langsung", "Apa yang terjadi kalau dosen pembimbing tidak membimbing?",
     "Dosen pembimbing mendapat teguran dari Koordinator Program Studi atau Koordinator PKL Program Studi bila tidak berkomunikasi dengan mahasiswa, "
     "dan SK-nya sebagai dosen pembimbing PKL dibatalkan bila tidak melaksanakan pembimbingan dari awal sampai akhir pelaksanaan PKL.",
     P(15), None),
    ("27", "Aspek penilaian", "Daftar", "Apa saja aspek yang dinilai dalam PKL?",
     "Penilaian PKL terdiri dari tiga aspek: aspek sikap (N1), aspek kompetensi profesional (N2), dan aspek seminar dan/atau laporan PKL (N3). "
     "Penilaian diberikan oleh dosen pembimbing lapangan di instansi dengan skala Likert 1 sampai 5.",
     P(16, 27) + K(4), None),
    ("28", "Konversi nilai", "Angka", "Nilai B+ itu berapa rentang angkanya?",
     "Nilai B+ setara rentang angka 76 sampai 80 dengan bobot 3,3.",
     P(16) + K(5), None),
    ("29", "Hubungan nilai dan kelulusan", "Angka, beberapa bagian", "Kalau nilai saya 74, apakah saya lulus PKL?",
     "Tidak. Nilai 74 termasuk rentang 71 sampai 75 yang setara nilai B (bobot 3,0), sedangkan syarat lulus PKL adalah nilai minimal B+ (76 sampai 80). "
     "Mahasiswa dengan nilai kurang dari B+ harus mengulang PKL.",
     P(11, 16) + K(5), None),
    ("30", "Parafrasa santai", "Parafrasa", "PKL-nya berapa bulan sih kak?",
     "PKL dilaksanakan minimal 4 bulan atau satu semester.",
     P(7, 14) + K(3), None),
    ("E1", "Sistem rujukan pustaka laporan", "Langsung", "Sistem rujukan pustaka apa yang dipakai dalam laporan PKL?",
     "Laporan PKL memakai sistem American Psychological Association (APA) dengan teknik rujukan berkurung (nama akhir, tahun). "
     "Kutipan langsung disertai nomor halaman, misalnya (Sugiyono, 2013: 47).",
     P(22) + K(6), None),
    ("E2", "Isi Bab I Pendahuluan laporan", "Daftar", "Apa saja isi Bab I Pendahuluan pada laporan PKL?",
     "Bab I Pendahuluan berisi latar belakang (alasan memilih bidang pekerjaan dan tempat PKL serta keterkaitannya dengan bidang studi), tujuan, manfaat, "
     "dan metode pelaksanaan (melalui observasi, partisipasi, dan evaluasi).",
     P(23, 25) + K(6), None),
    ("E3", "Dokumen lampiran laporan", "Daftar", "Dokumen apa saja yang harus dilampirkan pada laporan PKL?",
     "Lampiran laporan PKL memuat: surat permohonan PKL, lembar konsultasi pembimbingan PKL, penilaian PKL, daftar hadir, catatan mingguan PKL, biodata praktikan, "
     "surat keterangan atau sertifikat PKL dari perusahaan, dan berita acara.",
     P(24) + K(4), None),
    ("E4", "Urutan sistematika laporan", "Daftar, beberapa bagian", "Bagaimana contoh urutan sistematika laporan PKL?",
     "Contoh urutan sistematika laporan PKL: halaman judul, lembar persetujuan, kata pengantar, daftar isi, daftar gambar, daftar tabel, daftar lampiran, "
     "Bab I Pendahuluan (latar belakang, tujuan, manfaat, metode pelaksanaan), Bab II Pelaksanaan PKL (profil DUDI, lingkup pekerjaan, program pelaksanaan, jadwal pelaksanaan, pelaksanaan PKL), "
     "Bab III Studi Kasus atau Analisis Pekerjaan (analisis pekerjaan, hambatan dan solusi, pengembangan, kesimpulan, saran), daftar pustaka, dan lampiran. "
     "Sistematika dapat disesuaikan dengan ketentuan fakultas dan program studi.",
     P(22, 23, 25) + K(6, 7),
     "Buku Pedoman memuat tiga versi (Bab I sampai V pada ketentuan penulisan, empat bab pada uraian sistematika, tiga bab pada contoh daftar isi). Dokumen tambahan menutup dengan susunan Bab I Pendahuluan, Bab II Profil Instansi, "
     "Bab III Metode dan Pelaksanaan, Bab IV Pembahasan, Bab V Kesimpulan dan Saran. Mohon *Product Owner* menetapkan versi yang dipakai sebagai jawaban acuan."),
    ("E5", "Aspek nilai sikap (N1)", "Daftar", "Aspek apa saja yang dinilai pada nilai sikap (N1)?",
     "Nilai sikap (N1) menilai tujuh aspek: kerajinan atau kehadiran, tanggung jawab, prakarsa, kerja sama tim, kreativitas, kemandirian, dan penyesuaian dengan lingkungan. "
     "Nilai maksimalnya 35.",
     P(27) + K(4), None),
    ("E6", "Cara menghitung nilai akhir", "Angka, beberapa bagian", "Bagaimana cara menghitung nilai akhir PKL?",
     "Nilai setiap komponen dihitung dari jumlah nilai dibagi jumlah nilai maksimal lalu dikali 100, dengan nilai maksimal N1 (sikap) 35, N2 (kompetensi profesional) 25, dan N3 (seminar dan/atau laporan) 45. "
     "Nilai akhir = 30% N1 + 40% N2 + 30% N3.",
     P(16, 27, 28) + K(4, 5), None),
]

OUT_OF_PKL_BEHAVIOUR = (
    "Pertanyaan di luar topik PKL. Pekael tidak menjawab isinya, membalas dengan ramah, dan mengajak kembali bertanya seputar PKL."
)
NON_PKL = [
    ("N1", "Beasiswa", "Bagaimana cara mengajukan beasiswa di UNJ?",
     OUT_OF_PKL_BEHAVIOUR + " Untuk urusan akademik di luar PKL boleh disarankan bertanya ke Admin Prodi PTIK."),
    ("N2", "Pengetahuan umum", "Apa itu machine learning?", OUT_OF_PKL_BEHAVIOUR),
    ("N3", "Permintaan kreatif", "Buatkan saya puisi tentang kampus.", OUT_OF_PKL_BEHAVIOUR),
    ("N4", "Rekomendasi barang", "Laptop apa yang bagus untuk kuliah?", OUT_OF_PKL_BEHAVIOUR),
]


def page_text(source: str, page: int) -> str:
    if source == HANDBOOK:
        return (HANDBOOK_PAGES / f"page_{page:03d}.txt").read_text(encoding="utf-8").strip()
    import pymupdf

    with pymupdf.open(EXTRA_PDF) as pdf:
        return pdf[page - 1].get_text().strip()


def dataset_rows() -> list[dict]:
    rows = []
    for id_, topic, kind, question, reference, sources, note in PKL:
        rows.append({
            "id": id_, "version": VERSION, "category": "pkl", "topic": topic, "question_type": kind,
            "user_input": question, "reference": reference,
            "reference_contexts": [page_text(s, p) for s, p in sources],
            "reference_sources": [{"source_file": s, "page": p} for s, p in sources],
            "note": note,
        })
    for id_, topic, question, behaviour in NON_PKL:
        rows.append({
            "id": id_, "version": VERSION, "category": "non_pkl", "topic": topic, "question_type": "Di luar PKL",
            "user_input": question, "reference": behaviour, "reference_contexts": [], "reference_sources": [], "note": None,
        })
    return rows


CHECK = "☐ Sesuai   ☐ Perlu perbaikan, catatan: .............................."


def sheet() -> str:
    lines = [
        "# Lembar Validasi Dataset Evaluasi Pekael",
        "",
        "| | |",
        "|---|---|",
        "| Sprint | : Sprint 5 |",
        "| Dokumen sumber | : Buku Pedoman Praktik Kerja Lapangan UNJ 2025 dan dokumen Knowledge Base PKL Prodi PTIK UNJ dari *Product Owner* |",
        f"| Jumlah pertanyaan | : 40 ({len(PKL)} pertanyaan PKL, {len(NON_PKL)} pertanyaan di luar PKL) |",
        f"| Versi dataset | : {VERSION}, disusun {DRAFTED} |",
        "| Pemeriksa | : Bambang Satrio, S. Pd., M. Kom. (*Product Owner*) |",
        "",
        "## Tujuan",
        "",
        "Lembar ini memuat dataset evaluasi Pekael, yaitu 40 pertanyaan beserta jawaban acuannya. Dataset ini dipakai untuk evaluasi Ragas dan seluruh pengujian berikutnya, "
        "sehingga jawaban acuan harus benar menurut *Product Owner*. Pertanyaan no. 1 – 30 berasal dari daftar topik pertanyaan mahasiswa Sprint 1, E1 – E6 dari daftar pertanyaan uji Sprint 4, "
        "dan N1 – N4 adalah pertanyaan di luar topik PKL untuk menguji bahwa Pekael tidak menjawab hal di luar PKL.",
        "",
        "## Cara pemeriksaan",
        "",
        "1. Baca setiap pertanyaan dan jawaban acuannya.",
        "2. Beri tanda pada \"Sesuai\" bila jawaban acuan benar dan lengkap menurut ketentuan PKL di Prodi PTIK.",
        "3. Beri tanda pada \"Perlu perbaikan\" bila ada yang salah, kurang, atau berlebih, lalu tuliskan perbaikannya pada catatan.",
        "4. Untuk pertanyaan di luar PKL, periksa apakah perilaku yang diharapkan sudah tepat.",
        "5. Pertanyaan yang diberi catatan penyusun memerlukan keputusan *Product Owner*.",
        "",
        "## Ringkasan",
        "",
        "| Kelompok | Jumlah | Yang diperiksa |",
        "|---|---|---|",
        f"| Pertanyaan PKL | {len(PKL)} | Kebenaran dan kelengkapan jawaban acuan |",
        f"| Pertanyaan di luar PKL | {len(NON_PKL)} | Perilaku yang diharapkan |",
        "",
        "## Daftar pertanyaan",
        "",
        "| No | Topik | Pertanyaan | Jenis pertanyaan |",
        "|---|---|---|---|",
    ]
    lines += [f"| {i} | {t} | {q} | {k} |" for i, t, k, q, *_ in PKL]
    lines += [f"| {i} | {t} | {q} | Di luar PKL |" for i, t, q, _ in NON_PKL]
    lines += ["", "## Pertanyaan PKL dan jawaban acuan", "", "Pekael seharusnya menjawab sesuai jawaban acuan berikut.", ""]
    for id_, _, _, question, reference, _, note in PKL:
        lines += [f"**No. {id_}. {question}**", "", f"> {reference}", ""]
        if note:
            lines += [f"*Catatan penyusun: {note}*", ""]
        lines += [CHECK, ""]
    lines += ["## Pertanyaan di luar PKL", "", "Pekael seharusnya tidak menjawab isi pertanyaan berikut.", ""]
    for id_, _, question, behaviour in NON_PKL:
        lines += [f"**{id_}. {question}**", "", f"> Perilaku yang diharapkan: {behaviour}", "", CHECK, ""]
    lines += [
        "## Catatan *Product Owner*",
        "",
        "..............................................................................................................",
        "",
        "..............................................................................................................",
        "",
        "## Pernyataan validasi",
        "",
        "Saya telah memeriksa pertanyaan dan jawaban acuan pada lembar ini terhadap ketentuan PKL di Prodi PTIK. "
        "Dataset ini dinyatakan dapat dipakai untuk evaluasi Pekael setelah perbaikan yang dicatat di atas diterapkan.",
        "",
        "| | |",
        "|---|---|",
        "| Jakarta, ...........................<br>*Product Owner*,<br><br><br><br>Bambang Satrio, S. Pd., M. Kom.<br>NIP. {{NIP_PRODUCT_OWNER}} "
        "| <br>Developer,<br><br><br><br>Deni Merdiansyah<br>NIM {{NIM_DEVELOPER}} |",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    rows = dataset_rows()
    assert len(rows) == 40 and len({r["id"] for r in rows}) == 40
    assert all(";" not in r["reference"] for r in rows), "documents use no semicolons"
    DATASET.parent.mkdir(parents=True, exist_ok=True)
    DATASET.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    SHEET.parent.mkdir(parents=True, exist_ok=True)
    SHEET.write_text(sheet(), encoding="utf-8")
    pkl = sum(r["category"] == "pkl" for r in rows)
    print(f"{DATASET}: {len(rows)} entri ({pkl} PKL, {len(rows) - pkl} di luar PKL), versi {VERSION}")
    print(f"{SHEET}: lembar validasi")
    return 0


if __name__ == "__main__":
    sys.exit(main())
