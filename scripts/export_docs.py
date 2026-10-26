"""Export the Scrum documents (Markdown) to Word, and optionally PDF, using the Pekael report template.

The Markdown files stay the single source of truth. Every exported document shares one
layout (UNJ logo, research title, Times New Roman, A4) and only differs in the header
title and footer label. Output goes to docs/export/ (git-ignored).

Usage from the project root:
    .venv\\Scripts\\python.exe scripts\\export_docs.py              # all Scrum documents
    .venv\\Scripts\\python.exe scripts\\export_docs.py --sprint 1   # docs/scrum/sprint-01 only
    .venv\\Scripts\\python.exe scripts\\export_docs.py --pdf        # also save PDF (needs Microsoft Word)
    .venv\\Scripts\\python.exe scripts\\export_docs.py --build-reference "Lembar Validasi Sprint Planning 1.docx"

Personal identifiers are never stored in the repository: the placeholders {{NIM_DEVELOPER}}
and {{NIP_PRODUCT_OWNER}} in the Markdown are filled from .env when exporting.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[1]
SCRUM_DIR = ROOT / "docs" / "scrum"
EXPORT_DIR = ROOT / "docs" / "export"
REFERENCE_DOCX = ROOT / "docs" / "templates" / "reference.docx"
LUA_FILTER = ROOT / "docs" / "templates" / "pekael-docx.lua"
PERSONAL_PLACEHOLDERS = ("NIM_DEVELOPER", "NIP_PRODUCT_OWNER")
BLANK = "____________________"

# file stem -> (header title, header subtitle, footer label); {n} is the sprint number
SPRINT_DOCUMENTS = {
    "sprint_planning": (
        "LEMBAR VALIDASI SPRINT REPORT {n}",
        "Bagian A: Sprint Planning",
        "Lembar Validasi Sprint Report {n}: Sprint Planning",
    ),
    "sprint_review": (
        "LEMBAR VALIDASI SPRINT REPORT {n}",
        "Bagian B: Sprint Review",
        "Lembar Validasi Sprint Report {n}: Sprint Review",
    ),
    "sprint_retrospective": (
        "LEMBAR VALIDASI SPRINT REPORT {n}",
        "Bagian C: Sprint Retrospective",
        "Lembar Validasi Sprint Report {n}: Sprint Retrospective",
    ),
    "sprint_backlog": ("SPRINT REPORT {n}", "Logbook dan Sprint Backlog", "Sprint Report {n}: Logbook"),
    "pemeriksaan_ocr": (
        "SPRINT REPORT {n}",
        "Lampiran: Lembar Pemeriksaan Hasil OCR",
        "Sprint Report {n}: Pemeriksaan OCR",
    ),
    "topik_pertanyaan": (
        "SPRINT REPORT {n}",
        "Lampiran: Daftar Topik Pertanyaan Mahasiswa",
        "Sprint Report {n}: Topik Pertanyaan",
    ),
    "usulan_penyaringan": (
        "SPRINT REPORT {n}",
        "Lampiran: Usulan Penyaringan Isi Buku Pedoman",
        "Sprint Report {n}: Usulan Penyaringan",
    ),
}
OTHER_DOCUMENTS = {
    "product_backlog": ("PRODUCT BACKLOG", "Daftar Kebutuhan Produk Pekael", "Product Backlog"),
    "setup_phase": ("LAPORAN FASE SETUP", "Persiapan Lingkungan Pengembangan", "Laporan Fase Setup"),
}

FOOTER_XML = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    '<w:p><w:pPr><w:jc w:val="center"/></w:pPr>{run}'
    '<w:r>{rpr}<w:fldChar w:fldCharType="begin"/></w:r><w:r>{rpr}<w:instrText>PAGE</w:instrText></w:r>'
    '<w:r>{rpr}<w:fldChar w:fldCharType="separate"/></w:r><w:r>{rpr}<w:t>1</w:t></w:r>'
    '<w:r>{rpr}<w:fldChar w:fldCharType="end"/></w:r></w:p></w:ftr>'
)
FOOTER_RPR = '<w:rPr><w:color w:val="595959"/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>'

# Styles copied from the report template (Times New Roman 11 pt, headings with a rule, grey table grid).
STYLES = {
    "BodyText": '<w:style w:type="paragraph" w:styleId="BodyText"><w:name w:val="Body Text"/><w:basedOn w:val="Normal"/>'
    '<w:qFormat/><w:pPr><w:spacing w:before="0" w:after="80" w:line="276" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr></w:style>',
    "FirstParagraph": '<w:style w:type="paragraph" w:styleId="FirstParagraph"><w:name w:val="First Paragraph"/>'
    '<w:basedOn w:val="BodyText"/><w:next w:val="BodyText"/><w:qFormat/></w:style>',
    "Compact": '<w:style w:type="paragraph" w:styleId="Compact"><w:name w:val="Compact"/><w:basedOn w:val="BodyText"/>'
    '<w:qFormat/><w:pPr><w:spacing w:before="0" w:after="40" w:line="252" w:lineRule="auto"/><w:jc w:val="left"/></w:pPr>'
    '<w:rPr><w:sz w:val="21"/><w:szCs w:val="21"/></w:rPr></w:style>',
    "Heading1": '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>'
    '<w:next w:val="BodyText"/><w:uiPriority w:val="9"/><w:qFormat/><w:pPr><w:keepNext/><w:keepLines/>'
    '<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="2" w:color="404040"/></w:pBdr>'
    '<w:spacing w:before="240" w:after="120"/><w:outlineLvl w:val="0"/></w:pPr>'
    '<w:rPr><w:b/><w:bCs/><w:color w:val="000000"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>',
    "Heading2": '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/>'
    '<w:next w:val="BodyText"/><w:uiPriority w:val="9"/><w:unhideWhenUsed/><w:qFormat/><w:pPr><w:keepNext/><w:keepLines/>'
    '<w:spacing w:before="160" w:after="80"/><w:outlineLvl w:val="1"/></w:pPr>'
    '<w:rPr><w:b/><w:bCs/><w:color w:val="000000"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>',
    "Heading3": '<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/>'
    '<w:next w:val="BodyText"/><w:uiPriority w:val="9"/><w:unhideWhenUsed/><w:qFormat/><w:pPr><w:keepNext/><w:keepLines/>'
    '<w:spacing w:before="120" w:after="60"/><w:outlineLvl w:val="2"/></w:pPr>'
    '<w:rPr><w:b/><w:bCs/><w:i/><w:iCs/><w:color w:val="000000"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>',
    "BlockText": '<w:style w:type="paragraph" w:styleId="BlockText"><w:name w:val="Block Text"/><w:basedOn w:val="BodyText"/>'
    '<w:next w:val="BodyText"/><w:uiPriority w:val="9"/><w:unhideWhenUsed/><w:qFormat/><w:pPr><w:spacing w:before="60" w:after="120"/>'
    '<w:jc w:val="left"/></w:pPr><w:rPr><w:color w:val="404040"/><w:sz w:val="21"/><w:szCs w:val="21"/></w:rPr></w:style>',
    "Checklist": '<w:style w:type="paragraph" w:customStyle="1" w:styleId="Checklist"><w:name w:val="Checklist"/>'
    '<w:basedOn w:val="BodyText"/><w:qFormat/><w:pPr><w:spacing w:after="120" w:line="300" w:lineRule="auto"/>'
    '<w:jc w:val="left"/></w:pPr></w:style>',
    "VerbatimChar":'<w:style w:type="character" w:customStyle="1" w:styleId="VerbatimChar"><w:name w:val="Verbatim Char"/>'
    '<w:basedOn w:val="BodyTextChar"/><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr></w:style>',
    "Table": '<w:style w:type="table" w:default="1" w:styleId="Table"><w:name w:val="Table"/><w:basedOn w:val="TableNormal"/>'
    '<w:uiPriority w:val="99"/><w:tblPr><w:tblBorders>'
    + "".join(
        f'<w:{side} w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
        for side in ("top", "left", "bottom", "right", "insideH", "insideV")
    )
    + '</w:tblBorders><w:tblCellMar><w:top w:w="60" w:type="dxa"/><w:left w:w="100" w:type="dxa"/>'
    '<w:bottom w:w="60" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tblCellMar></w:tblPr>'
    '<w:tcPr><w:vAlign w:val="center"/></w:tcPr>'
    '<w:tblStylePr w:type="firstRow"><w:pPr><w:jc w:val="center"/></w:pPr>'
    '<w:rPr><w:b/><w:bCs/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:tblStylePr></w:style>',
}
DOC_DEFAULTS = (
    '<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" w:eastAsia="Times New Roman" '
    'w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:sz w:val="22"/><w:szCs w:val="22"/>'
    '<w:lang w:val="id-ID" w:eastAsia="en-US" w:bidi="ar-SA"/></w:rPr></w:rPrDefault>'
    '<w:pPrDefault><w:pPr><w:spacing w:after="80"/></w:pPr></w:pPrDefault></w:docDefaults>'
)
SECT_PR = (
    '<w:sectPr><w:headerReference w:type="default" r:id="rIdPekaelHeader"/>'
    '<w:footerReference w:type="default" r:id="rIdPekaelFooter"/><w:pgSz w:w="11906" w:h="16838"/>'
    '<w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" w:header="708" w:footer="708" w:gutter="0"/>'
    "</w:sectPr>"
)
RELS_HEADER = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/header"
RELS_FOOTER = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer"
CT_HEADER = "application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"
CT_FOOTER = "application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"


def find_pandoc() -> str:
    found = shutil.which("pandoc")
    candidates = [found] if found else []
    candidates.append(os.path.join(os.environ.get("LOCALAPPDATA", ""), "Pandoc", "pandoc.exe"))
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return candidate
    raise SystemExit("pandoc tidak ditemukan. Pasang dengan: winget install --id JohnMacFarlane.Pandoc --exact")


def _rewrite_zip(source: Path, target: Path, replace: dict[str, bytes]) -> None:
    """Copy a zip, replacing or adding the given members."""
    with zipfile.ZipFile(source) as zin, zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename not in replace:
                zout.writestr(item, zin.read(item.filename))
        for name, data in replace.items():
            zout.writestr(name, data)


def build_reference(template_docx: Path) -> None:
    """Create docs/templates/reference.docx: pandoc's reference + the template's header, logo, page setup and styles.

    Only layout is taken from the template, never its body text (which contains personal data).
    """
    pandoc = find_pandoc()
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp) / "pandoc-reference.docx"
        subprocess.run([pandoc, "-o", str(base), "--print-default-data-file", "reference.docx"], check=True)
        with zipfile.ZipFile(template_docx) as tpl, zipfile.ZipFile(base) as ref:
            header = tpl.read("word/header1.xml").decode("utf-8")
            header_rels = tpl.read("word/_rels/header1.xml.rels")
            image_target = re.search(r'Target="media/([^"]+)"', header_rels.decode("utf-8")).group(1)
            image = tpl.read(f"word/media/{image_target}")
            compat = re.search(r"<w:compat>.*?</w:compat>", tpl.read("word/settings.xml").decode("utf-8"), re.S)
            settings = ref.read("word/settings.xml").decode("utf-8")
            styles = ref.read("word/styles.xml").decode("utf-8")
            document = ref.read("word/document.xml").decode("utf-8")
            doc_rels = ref.read("word/_rels/document.xml.rels").decode("utf-8")
            content_types = ref.read("[Content_Types].xml").decode("utf-8")

        title_runs = re.findall(r"<w:t>([^<]+)</w:t>", header)
        if len(title_runs) < 2:
            raise SystemExit("Header template tidak berisi judul dan sub-judul yang dikenali")
        header = header.replace(f"<w:t>{title_runs[0]}</w:t>", "<w:t>{{HEADER_TITLE}}</w:t>", 1)
        header = header.replace(f"<w:t>{title_runs[1]}</w:t>", "<w:t>{{HEADER_SUBTITLE}}</w:t>", 1)

        # Word 2013+ layout mode, so the header text wraps around the logo exactly as in the template.
        if compat and "<w:compat>" not in settings:
            anchor = "<w:rsids" if "<w:rsids" in settings else "<m:mathPr"
            settings = settings.replace(anchor, compat.group(0) + anchor, 1)
        styles = re.sub(r"<w:docDefaults>.*?</w:docDefaults>", DOC_DEFAULTS, styles, count=1, flags=re.S)
        for style_id, xml in STYLES.items():
            styles, count = re.subn(
                rf'<w:style [^>]*w:styleId="{style_id}"[^>]*>.*?</w:style>', lambda _: xml, styles, count=1, flags=re.S
            )
            if count == 0:
                styles = styles.replace("</w:styles>", xml + "</w:styles>")
        document = re.sub(r"<w:sectPr>.*?</w:sectPr>", SECT_PR, document, flags=re.S)
        doc_rels = doc_rels.replace(
            "</Relationships>",
            f'<Relationship Id="rIdPekaelHeader" Type="{RELS_HEADER}" Target="header1.xml"/>'
            f'<Relationship Id="rIdPekaelFooter" Type="{RELS_FOOTER}" Target="footer1.xml"/></Relationships>',
        )
        if 'Extension="png"' not in content_types:
            content_types = content_types.replace("</Types>", '<Default Extension="png" ContentType="image/png"/></Types>')
        content_types = content_types.replace(
            "</Types>",
            f'<Override PartName="/word/header1.xml" ContentType="{CT_HEADER}"/>'
            f'<Override PartName="/word/footer1.xml" ContentType="{CT_FOOTER}"/></Types>',
        )
        footer = FOOTER_XML.format(run=f'<w:r>{FOOTER_RPR}<w:t xml:space="preserve">{{{{FOOTER_LABEL}}}} | Halaman </w:t></w:r>', rpr=FOOTER_RPR)

        REFERENCE_DOCX.parent.mkdir(parents=True, exist_ok=True)
        _rewrite_zip(
            base,
            REFERENCE_DOCX,
            {
                "word/styles.xml": styles.encode("utf-8"),
                "word/settings.xml": settings.encode("utf-8"),
                "word/document.xml": document.encode("utf-8"),
                "word/_rels/document.xml.rels": doc_rels.encode("utf-8"),
                "[Content_Types].xml": content_types.encode("utf-8"),
                "word/header1.xml": header.encode("utf-8"),
                "word/_rels/header1.xml.rels": header_rels,
                f"word/media/{image_target}": image,
                "word/footer1.xml": footer.encode("utf-8"),
            },
        )
    print(f"Template dibuat: {REFERENCE_DOCX.relative_to(ROOT)}")


def document_titles(md_path: Path) -> tuple[str, str, str] | None:
    """Header title, subtitle and footer label for a Scrum document, or None to skip it."""
    stem = md_path.stem
    sprint = re.fullmatch(r"sprint-(\d+)", md_path.parent.name)
    if sprint and stem in SPRINT_DOCUMENTS:
        n = int(sprint.group(1))
        return tuple(part.format(n=n) for part in SPRINT_DOCUMENTS[stem])
    if stem in OTHER_DOCUMENTS:
        return OTHER_DOCUMENTS[stem]
    return None


def _personal_values() -> dict[str, str]:
    env = {**dotenv_values(ROOT / ".env"), **os.environ}
    return {name: (env.get(name) or "").strip() or BLANK for name in PERSONAL_PLACEHOLDERS}


def export_document(md_path: Path, pandoc: str, personal: dict[str, str]) -> Path:
    title, subtitle, footer = document_titles(md_path)
    markdown = md_path.read_text(encoding="utf-8")
    for name, value in personal.items():
        markdown = markdown.replace("{{" + name + "}}", value)

    out = EXPORT_DIR / md_path.relative_to(SCRUM_DIR).with_suffix(".docx")
    out.parent.mkdir(parents=True, exist_ok=True)
    raw = out.with_suffix(".pandoc.docx")
    subprocess.run(
        [pandoc, "-f", "gfm", "-t", "docx", "--reference-doc", str(REFERENCE_DOCX), "--lua-filter", str(LUA_FILTER),
         "--columns", "10000", "-o", str(raw)],
        input=markdown.encode("utf-8"),
        check=True,
    )

    values = {"{{HEADER_TITLE}}": title, "{{HEADER_SUBTITLE}}": subtitle, "{{FOOTER_LABEL}}": footer}
    replace = {}
    with zipfile.ZipFile(raw) as docx:
        for name in docx.namelist():
            if re.fullmatch(r"word/(header|footer)\d+\.xml", name):
                xml = docx.read(name).decode("utf-8")
                for placeholder, value in values.items():
                    xml = xml.replace(placeholder, escape(value))
                replace[name] = xml.encode("utf-8")
        replace["word/document.xml"] = _format_tables(docx.read("word/document.xml").decode("utf-8")).encode("utf-8")
    _rewrite_zip(raw, out, replace)
    raw.unlink()
    return out


def _format_tables(document: str) -> str:
    """Stretch tables to the text width. Signature tables and label/value tables (no header row) get no borders."""

    def fix(match: re.Match) -> str:
        table = re.sub(r'<w:tblW [^>]*/>', '<w:tblW w:type="pct" w:w="5000"/>', match.group(0), count=1)
        text = "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", table))
        is_signature = "Product Owner" in text and "Developer" in text and ("NIM" in text or "NIP" in text)
        if is_signature or "<w:tblHeader" not in table:
            no_borders = "<w:tblBorders>" + "".join(
                f'<w:{side} w:val="nil"/>' for side in ("top", "left", "bottom", "right", "insideH", "insideV")
            ) + "</w:tblBorders>"
            table = table.replace("</w:tblPr>", no_borders + "</w:tblPr>", 1)
        return table

    return re.sub(r"<w:tbl>.*?</w:tbl>", fix, document, flags=re.S)


PDF_SCRIPT = r"""
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    foreach ($path in $args) {
        $doc = $word.Documents.Open($path, $false, $true)
        $doc.Fields.Update() | Out-Null
        $doc.SaveAs([ref]([IO.Path]::ChangeExtension($path, '.pdf')), [ref]17)
        $doc.Close([ref]$false)
    }
} finally { $word.Quit() }
"""


def to_pdf(docx_files: list[Path]) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        script = Path(tmp) / "docx_to_pdf.ps1"
        script.write_text(PDF_SCRIPT, encoding="utf-8")
        subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script), *map(str, docx_files)],
            check=True,
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--sprint", type=int, help="export only docs/scrum/sprint-NN")
    parser.add_argument("--pdf", action="store_true", help="also save PDF through Microsoft Word")
    parser.add_argument("--build-reference", metavar="TEMPLATE_DOCX", help="rebuild docs/templates/reference.docx")
    args = parser.parse_args()

    if args.build_reference:
        build_reference(Path(args.build_reference))
        return 0
    if not REFERENCE_DOCX.is_file():
        raise SystemExit(f"{REFERENCE_DOCX.relative_to(ROOT)} belum ada. Jalankan dengan --build-reference <template.docx>")

    folder = SCRUM_DIR / f"sprint-{args.sprint:02d}" if args.sprint else SCRUM_DIR
    sources = [p for p in sorted(folder.rglob("*.md")) if "templates" not in p.parts and document_titles(p)]
    if not sources:
        raise SystemExit(f"Tidak ada dokumen untuk diekspor di {folder.relative_to(ROOT)}")

    pandoc, personal = find_pandoc(), _personal_values()
    exported = [export_document(path, pandoc, personal) for path in sources]
    for path in exported:
        print(f"Word: {path.relative_to(ROOT)}")
    if args.pdf:
        to_pdf(exported)
        for path in exported:
            print(f"PDF : {path.with_suffix('.pdf').relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
