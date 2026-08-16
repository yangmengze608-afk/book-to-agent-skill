"""Ingest: extract plain text from .pdf / .epub / .txt / .md files.

Deterministic, no OCR. Scanned PDFs are detected and flagged
(`ocr_required`) with an extension point for future OCR providers.
"""

import re
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from typing import List, Optional, Tuple
from urllib.parse import unquote

from .models import Book, Chapter, SourceMeta
from .structure import detect_chapters, detect_meta
from .util import sha256_file, word_count

SUPPORTED_FORMATS = (".pdf", ".epub", ".txt", ".md")

# Below this many extractable characters per page, a PDF is almost
# certainly a scan (or image-only) and needs OCR.
_PDF_CHARS_PER_PAGE_THRESHOLD = 100


class IngestError(Exception):
    pass


class OcrRequiredError(IngestError):
    """Raised when strict=True and the PDF has no text layer."""


# --------------------------------------------------------------------- PDF

def extract_pdf(path: Path, strict: bool = False) -> Tuple[str, bool]:
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    pages: List[str] = []
    for page in reader.pages:
        try:
            pages.append(page.extract_text() or "")
        except Exception:
            pages.append("")
    text = "\n\n".join(p.strip() for p in pages if p.strip())
    ocr = len(pages) > 0 and len(text) / max(1, len(pages)) < _PDF_CHARS_PER_PAGE_THRESHOLD
    if ocr and strict:
        raise OcrRequiredError(
            f"{path.name}: PDF appears to be scanned (no text layer). "
            "OCR is required but intentionally out of scope for V1; "
            "see README 'Limitations'."
        )
    return text, ocr


# -------------------------------------------------------------------- EPUB

class _HtmlToText(HTMLParser):
    _SKIP = {"style", "script", "head", "title", "svg"}
    _BLOCK = {
        "p", "div", "h1", "h2", "h3", "h4", "h5", "h6",
        "li", "tr", "section", "article", "blockquote", "pre",
    }

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: List[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self._SKIP:
            self._skip_depth += 1
        elif tag == "br":
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in self._SKIP and self._skip_depth > 0:
            self._skip_depth -= 1
        elif tag in self._BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self._skip_depth and data.strip():
            self.parts.append(data)

    def text(self) -> str:
        raw = "".join(self.parts)
        lines = [ln.strip() for ln in raw.splitlines()]
        return "\n".join(ln for ln in lines if ln)


def _attr(tag: str, name: str) -> Optional[str]:
    m = re.search(rf'{name}\s*=\s*"([^"]*)"', tag)
    if m:
        return m.group(1)
    m = re.search(rf"{name}\s*=\s*'([^']*)'", tag)
    return m.group(1) if m else None


def extract_epub(path: Path) -> Tuple[str, str, str]:
    """Returns (text, title_hint, author_hint)."""
    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        container = "META-INF/container.xml"
        if container not in names:
            raise IngestError(f"{path.name}: missing META-INF/container.xml")
        container_xml = zf.read(container).decode("utf-8", "ignore")
        m = re.search(r'full-path\s*=\s*"([^"]+)"', container_xml)
        if not m:
            raise IngestError(f"{path.name}: cannot find OPF path in container.xml")
        opf_path = unquote(m.group(1))
        if opf_path not in names:
            raise IngestError(f"{path.name}: OPF not found at {opf_path}")
        opf = zf.read(opf_path).decode("utf-8", "ignore")

        tm = re.search(r"<dc:title[^>]*>(.*?)</dc:title>", opf, re.DOTALL | re.I)
        am = re.search(r"<dc:creator[^>]*>(.*?)</dc:creator>", opf, re.DOTALL | re.I)
        title_hint = tm.group(1).strip() if tm else ""
        author_hint = am.group(1).strip() if am else ""

        # manifest id -> (href, media-type)
        items = {}
        for tag_m in re.finditer(r"<item\b[^>]*>", opf):
            tag = tag_m.group(0)
            iid, href, mtype = _attr(tag, "id"), _attr(tag, "href"), _attr(tag, "media-type")
            if iid and href:
                items[iid] = (unquote(href), mtype or "")
        # spine order
        spine = re.findall(r'<itemref\b[^>]*idref\s*=\s*"([^"]+)"', opf)
        opf_dir = "/".join(opf_path.split("/")[:-1])

        parts: List[str] = []
        for idref in spine:
            href, mtype = items.get(idref, (None, None))
            if not href:
                continue
            if mtype and mtype not in (
                "application/xhtml+xml", "text/html", "application/xml",
            ):
                continue
            full = f"{opf_dir}/{href}" if opf_dir else href
            if full not in names:
                continue
            html = zf.read(full).decode("utf-8", "ignore")
            parser = _HtmlToText()
            try:
                parser.feed(html)
            except Exception:
                continue
            chunk = parser.text()
            if chunk:
                parts.append(chunk)
        if not parts:
            # fallback: process any xhtml in the zip
            for name in names:
                if name.endswith((".xhtml", ".html", ".htm")):
                    parser = _HtmlToText()
                    try:
                        parser.feed(zf.read(name).decode("utf-8", "ignore"))
                    except Exception:
                        continue
                    chunk = parser.text()
                    if chunk:
                        parts.append(chunk)
        return "\n\n".join(parts), title_hint, author_hint


# ----------------------------------------------------------------- plain

def extract_plain(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")


# ----------------------------------------------------------------- public

def ingest(path: Path, strict_ocr: bool = False) -> Book:
    path = Path(path)
    if not path.exists():
        raise IngestError(f"file not found: {path}")
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_FORMATS:
        raise IngestError(
            f"unsupported format '{suffix}'. Supported: {', '.join(SUPPORTED_FORMATS)}"
        )

    ocr_required = False
    title_hint = author_hint = ""
    if suffix == ".pdf":
        text, ocr_required = extract_pdf(path, strict=strict_ocr)
    elif suffix == ".epub":
        text, title_hint, author_hint = extract_epub(path)
    else:
        text = extract_plain(path)

    chapters: List[Chapter] = detect_chapters(text, suffix.lstrip("."))
    if not title_hint:
        t, a = detect_meta(text, suffix.lstrip("."))
        title_hint, author_hint = t or "", a or ""

    meta = SourceMeta(
        original_path=str(path),
        format=suffix.lstrip("."),
        sha256=sha256_file(path),
        word_count=word_count(text),
        chapter_count=len(chapters),
        ocr_required=ocr_required,
        notes="scanned pdf detected; OCR out of scope for V1" if ocr_required else "",
    )
    return Book(
        path=path,
        fmt=suffix.lstrip("."),
        text=text,
        chapters=chapters,
        title_hint=title_hint,
        author_hint=author_hint,
        ocr_required=ocr_required,
        source_meta=meta,
    )
