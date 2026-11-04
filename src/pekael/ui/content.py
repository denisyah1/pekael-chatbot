"""Texts shown on the student page.

Every fact quotes the handbook (Buku Pedoman PKL UNJ 2025) with its PDF page, checked
against the verified page text. Wording stays plain and casual, without "AI" terms.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Fact:
    figure: str
    text: str
    page: int


FACTS = (
    Fact("100 SKS", "Syarat minimal SKS untuk bisa menjadi peserta PKL.", 10),
    Fact("4 bulan", "Lama minimal pelaksanaan PKL, atau satu semester.", 14),
    Fact("B+", "Nilai minimal dari pembimbing lapangan dan dosen pembimbing agar lulus PKL.", 11),
    Fact("6 SKS", "Bobot PKL sesuai aturan UNJ, atau diatur oleh program studi.", 13),
    Fact("30 · 40 · 30", "Nilai akhir = 30% sikap (N1) + 40% kompetensi profesional (N2) + 30% seminar dan laporan (N3).", 28),
    Fact("8 dokumen", "Lampiran wajib laporan PKL, dari surat permohonan sampai berita acara.", 24),
)

EXAMPLES = (
    "Apa saja syarat untuk bisa ikut PKL?",
    "Bagaimana langkah-langkah mengajukan PKL?",
    "Kalau nilai saya 74, apakah saya lulus PKL?",
    "Dokumen apa saja yang dilampirkan di laporan PKL?",
)

# Progress text for each Chain step (pekael.core.rag_steps)
STEP_LABELS = {
    "validate_input": "Membaca pertanyaanmu",
    "retrieve": "Membuka buku pedoman",
    "relevancy_gate": "Memilih halaman yang paling sesuai",
    "build_prompt": "Mengumpulkan kutipan",
    "generate": "Menyusun jawaban",
    "validate_citations": "Mencocokkan nomor halaman",
}

SLOW_HINT = "Bagian ini kadang lebih lama saat layanan sedang ramai, mohon ditunggu."

INTRO_LINES = (
    "Teman tanya seputar Praktik Kerja Lapangan.",
    "Semua jawabannya diambil dari Buku Pedoman PKL UNJ, lengkap dengan halamannya.",
)
GREETING = "Halo, mau tahu apa soal PKL?"
GREETING_SUB = "Tulis pertanyaanmu dengan bahasa sehari-hari. Pekael akan mencarinya di buku pedoman dan menunjukkan halamannya."
PLACEHOLDER = "Tulis pertanyaanmu tentang PKL..."
NOTE = "Pekael bisa keliru. Untuk keputusan resmi, cek buku pedoman atau tanya koordinator PKL."
HOW_IT_WORKS = (
    ("Kamu bertanya", "Pakai bahasa sehari-hari, satu pertanyaan sekali kirim."),
    ("Pekael membuka buku", "Halaman yang paling sesuai dicari dari Buku Pedoman PKL."),
    ("Jawaban + halaman", "Setiap jawaban menyebut halaman sumbernya, jadi bisa kamu cek sendiri."),
)
NOT_CONFIGURED = "Pekael belum bisa dipakai karena pengaturannya belum lengkap. Silakan hubungi admin."
NOT_READY = "Buku pedoman belum dimuat ke Pekael, jadi pertanyaan belum bisa dijawab. Silakan hubungi admin."
