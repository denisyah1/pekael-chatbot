import pytest
from langchain_core.documents import Document

from pekael.splitters.factory import DocumentSplitterFactory
from pekael.splitters.recursive_character_splitter import RecursiveCharacterSplitter


def _page(page: int, text: str) -> Document:
    return Document(
        page_content=text,
        metadata={"source_file": "pedoman.pdf", "source_hash": "abcdef0123456789", "page": page, "extraction_method": "tesseract_ocr"},
    )


LONG_PARAGRAPH = " ".join(f"Kalimat ke-{i} tentang pelaksanaan PKL di instansi mitra." for i in range(1, 40))


def test_short_page_becomes_one_chunk_with_metadata():
    (chunk,) = RecursiveCharacterSplitter(1000, 150).split([_page(7, "1. Waktu pelaksanaan PKL minimal 4 bulan.")])

    assert chunk.page_content == "1. Waktu pelaksanaan PKL minimal 4 bulan."
    assert chunk.metadata["source_file"] == "pedoman.pdf"
    assert chunk.metadata["page"] == 7
    assert chunk.metadata["chunk_id"] == "abcdef01-p007-c01"
    assert chunk.metadata["chunk_index"] == 1
    assert "start_index" not in chunk.metadata


def test_long_text_respects_size_and_overlap():
    splitter = RecursiveCharacterSplitter(chunk_size=300, chunk_overlap=60)

    chunks = splitter.split([_page(5, LONG_PARAGRAPH)])

    assert len(chunks) > 1
    assert all(len(c.page_content) <= 300 for c in chunks)
    first_tail = chunks[0].page_content[-30:]
    assert first_tail.split(" ", 1)[-1] in chunks[1].page_content  # neighbouring chunks overlap


def test_chunk_ids_are_unique_and_stable():
    pages = [_page(4, LONG_PARAGRAPH), _page(5, LONG_PARAGRAPH)]
    splitter = RecursiveCharacterSplitter(300, 50)

    first = [c.metadata["chunk_id"] for c in splitter.split(pages)]
    second = [c.metadata["chunk_id"] for c in splitter.split(pages)]

    assert first == second
    assert len(set(first)) == len(first)


def test_empty_pages_are_skipped():
    chunks = RecursiveCharacterSplitter(1000, 150).split([_page(1, "   "), _page(2, "Isi halaman dua.")])

    assert [c.metadata["page"] for c in chunks] == [2]


def test_chunks_never_span_two_pages():
    chunks = RecursiveCharacterSplitter(1000, 150).split([_page(5, "akhir halaman lima, disiplin, dan"), _page(6, "bertanggung jawab dalam tugas.")])

    assert [(c.metadata["page"], c.page_content) for c in chunks] == [
        (5, "akhir halaman lima, disiplin, dan"),
        (6, "bertanggung jawab dalam tugas."),
    ]


def test_section_comes_from_nearest_heading_and_carries_to_next_page():
    page_10 = "p. Menyerahkan laporan.\n\nG. Persyaratan Peserta PKL\n\n1. Mahasiswa memenuhi minimal 100 SKS."
    page_11 = "e. Memperoleh izin orang tua.\n\nH. Syarat Kelulusan PKL\n\nMahasiswa dinyatakan lulus apabila nilai minimal B+."
    splitter = RecursiveCharacterSplitter(chunk_size=60, chunk_overlap=0)

    chunks = splitter.split([_page(10, page_10), _page(11, page_11)])

    def section_of(text: str) -> str:
        return next(c.metadata["section"] for c in chunks if text in c.page_content)

    assert section_of("minimal 100 SKS") == "G. Persyaratan Peserta PKL"
    assert section_of("izin orang tua") == "G. Persyaratan Peserta PKL"  # page 11 starts inside section G
    assert section_of("nilai minimal B+") == "H. Syarat Kelulusan PKL"
    assert section_of("Menyerahkan laporan") == ""


def test_chunk_spanning_sections_lists_all_of_them():
    text = "lanjutan bagian A.\n\nB. Prosedur Pelaksanaan PKL\n\n1. Mengajukan permohonan.\n\nC. Sanksi\n\na. Teguran."
    pages = [_page(14, "A. Prosedur Administrasi\n\nisi."), _page(15, text)]

    chunk = RecursiveCharacterSplitter(1000, 0).split(pages)[1]

    assert chunk.metadata["section"] == "A. Prosedur Administrasi / B. Prosedur Pelaksanaan PKL / C. Sanksi"


def test_chapter_heading_starts_a_new_section():
    pages = [_page(15, "C. Sanksi\n\nb. Pembatalan SK."), _page(16, "BAB III\nSISTEM PENILAIAN\n\nUntuk mengetahui keberhasilan.")]

    chunks = RecursiveCharacterSplitter(1000, 0).split(pages)

    assert chunks[1].metadata["section"] == "BAB III SISTEM PENILAIAN"


def test_list_items_are_not_mistaken_for_headings():
    chunks = RecursiveCharacterSplitter(1000, 0).split([_page(8, "a. Menjalin kerja sama dengan instansi.\nb. Membina program PKL.")])

    assert chunks[0].metadata["section"] == ""


def test_factory_builds_working_splitter():
    splitter = DocumentSplitterFactory.get_splitter("recursive_character", chunk_size=500, chunk_overlap=50)

    assert splitter.split([_page(1, "Teks singkat.")])[0].page_content == "Teks singkat."


@pytest.mark.parametrize(("size", "overlap"), [(0, 0), (100, 100), (100, -1)])
def test_invalid_parameters(size, overlap):
    with pytest.raises(ValueError):
        RecursiveCharacterSplitter(size, overlap)
