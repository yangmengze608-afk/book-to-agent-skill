"""8. Extraction fallback behavior: txt/md/epub/pdf ingest paths."""

import zipfile

import pytest

from book_to_agent_skill.ingest import (
    IngestError,
    OcrRequiredError,
    extract_pdf,
    ingest,
)


def test_unsupported_format_rejected(tmp_path):
    bad = tmp_path / "book.docx"
    bad.write_text("x")
    with pytest.raises(IngestError, match="unsupported format"):
        ingest(bad)


def test_missing_file_rejected(tmp_path):
    with pytest.raises(IngestError, match="not found"):
        ingest(tmp_path / "nope.pdf")


def test_md_ingest_chapters(example_book):
    book = ingest(example_book)
    assert book.fmt == "md"
    assert not book.ocr_required
    assert len(book.chapters) == 8
    assert not any(c.synthetic for c in book.chapters)
    assert "Every Decision Is a Bet" in book.chapter_titles()[0]
    assert book.title_hint == "The Decision Notebook"
    assert book.source_meta.sha256 and len(book.source_meta.sha256) == 64


def test_txt_without_headings_falls_back_to_synthetic_chapters(tmp_path):
    """No headings -> structure detection must still produce chunks."""
    txt = tmp_path / "plain.txt"
    words = "decision bet belief uncertainty " * 400  # ~2000 words
    txt.write_text(words)
    book = ingest(txt)
    assert book.chapters, "fallback must produce synthetic chapters"
    assert all(c.synthetic for c in book.chapters)
    assert book.source_meta.chapter_count == len(book.chapters)


def test_epub_ingest_with_spine_and_fallback(tmp_path):
    """A minimal valid epub extracts via spine; one without container.xml
    is rejected; one with html but no spine falls back to any xhtml."""
    def make_epub(path, with_container=True, with_spine=True):
        opf = '<?xml version="1.0"?><package xmlns:dc="http://purl.org/dc/elements/1.1/">'
        opf += "<metadata><dc:title>Test Book</dc:title>"
        opf += "<dc:creator>Test Author</dc:creator></metadata><manifest>"
        opf += '<item id="c1" href="c1.xhtml" media-type="application/xhtml+xml"/>'
        opf += "</manifest>"
        if with_spine:
            opf += '<spine><itemref idref="c1"/></spine>'
        opf += "</package>"
        chapter = ("<html><body><h1>Chapter One</h1>"
                   "<p>decision bets under uncertainty</p></body></html>")
        with zipfile.ZipFile(path, "w") as zf:
            if with_container:
                zf.writestr(
                    "META-INF/container.xml",
                    '<?xml version="1.0"?><container>'
                    '<rootfile full-path="content.opf" '
                    'media-type="application/oebps-package+xml"/></container>',
                )
            zf.writestr("content.opf", opf)
            zf.writestr("c1.xhtml", chapter)

    good = tmp_path / "good.epub"
    make_epub(good)
    book = ingest(good)
    assert book.fmt == "epub"
    assert book.title_hint == "Test Book"
    assert book.author_hint == "Test Author"
    assert "decision bets" in book.text

    no_spine = tmp_path / "nospine.epub"
    make_epub(no_spine, with_spine=False)
    book2 = ingest(no_spine)
    assert "decision bets" in book2.text, "no-spine epub must use fallback"

    no_container = tmp_path / "bad.epub"
    make_epub(no_container, with_container=False)
    with pytest.raises(IngestError, match="container.xml"):
        ingest(no_container)


def test_scanned_pdf_detected(tmp_path):
    """A PDF with no extractable text must be flagged, and strict mode
    must raise the OCR error (V1 does not OCR)."""
    from pypdf import PdfWriter

    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    scanned = tmp_path / "scanned.pdf"
    with open(scanned, "wb") as f:
        writer.write(f)

    text, ocr = extract_pdf(scanned)
    assert text == ""
    assert ocr is True

    book = ingest(scanned)
    assert book.ocr_required is True
    assert "OCR" in book.source_meta.notes

    with pytest.raises(OcrRequiredError):
        ingest(scanned, strict_ocr=True)
