from pekael.loaders.text_cleaning import clean_page_text


def test_empty_and_whitespace_only_text():
    assert clean_page_text("") == ""
    assert clean_page_text("  \n\n \t \n") == ""


def test_wrapped_lines_are_joined_into_one_paragraph():
    raw = "Praktik Kerja Lapangan (PKL) merupakan\nkegiatan kurikuler yang\ndilaksanakan di luar kampus."

    assert clean_page_text(raw) == "Praktik Kerja Lapangan (PKL) merupakan kegiatan kurikuler yang dilaksanakan di luar kampus."


def test_paragraph_breaks_are_kept():
    raw = "Paragraf pertama selesai.\n\nParagraf kedua dimulai."

    assert clean_page_text(raw) == "Paragraf pertama selesai.\n\nParagraf kedua dimulai."


def test_list_items_stay_on_their_own_lines():
    raw = "Tujuan PKL adalah:\n1. Menyiapkan mahasiswa\nagar berpengalaman;\n2. Memberikan kesempatan;\na. butir huruf\nb) butir lain\n- butir strip"

    assert clean_page_text(raw).split("\n") == [
        "Tujuan PKL adalah:",
        "1. Menyiapkan mahasiswa agar berpengalaman;",
        "2. Memberikan kesempatan;",
        "a. butir huruf",
        "b) butir lain",
        "- butir strip",
    ]


def test_heading_is_not_merged_into_following_paragraph():
    raw = "8. Penggunaan Angka Desimal\nUntuk penulisan angka desimal, angka dalam penulisan laporan PKL menggunakan\npembulatan dua angka."

    assert clean_page_text(raw).split("\n") == [
        "8. Penggunaan Angka Desimal",
        "Untuk penulisan angka desimal, angka dalam penulisan laporan PKL menggunakan pembulatan dua angka.",
    ]


def test_long_line_followed_by_capitalised_word_is_still_joined():
    raw = "dimana setiap perguruan tinggi diharapkan dapat melakukan transformasi sejalan dengan\nIndikator Kinerja Utama (IKU)."

    assert "\n" not in clean_page_text(raw)


def test_table_rows_stay_on_their_own_lines():
    raw = "Tingkat Penguasaan | Nilai | Bobot\n86-100 | A | 4\n76-80 | B+ | 3,3"

    assert clean_page_text(raw) == raw


def test_cleaning_is_idempotent_on_cleaned_text():
    raw = "A. Judul\n\nKalimat panjang yang\nterbungkus.\n1. butir satu\n2. butir dua\n\nTingkat | Nilai\n86-100 | A"
    once = clean_page_text(raw)

    assert clean_page_text(once) == once


def test_blank_line_inside_a_sentence_is_rejoined():
    raw = "sesuai dengan bidang\n\nkeilmuan/program studinya."

    assert clean_page_text(raw) == "sesuai dengan bidang keilmuan/program studinya."


def test_new_paragraph_after_finished_sentence_is_not_joined():
    assert clean_page_text("Kalimat selesai.\n\nlanjutan huruf kecil") == "Kalimat selesai.\n\nlanjutan huruf kecil"
    assert clean_page_text("profesional, disiplin, dan\n\n4. Mengembangkan") == "profesional, disiplin, dan\n\n4. Mengembangkan"


def test_numbers_punctuation_and_hyphens_are_preserved():
    raw = "Kepmendikbud Nomor 754/P/2020, IKU2; seluas-luasnya; hard-skill (20 SKS) 3,5%"

    assert clean_page_text(raw) == raw


def test_layout_noise_is_normalised():
    raw = "Kata dengan   spasi  ganda\t dan ﬁle­   \r\nbaris windows\fhalaman"

    assert clean_page_text(raw) == "Kata dengan spasi ganda dan file baris windows halaman"
