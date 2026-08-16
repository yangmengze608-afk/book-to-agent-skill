"""Structure detection: split raw text into chapters."""

import re
from typing import List, Optional, Tuple

from .models import Chapter

_MD_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$", re.MULTILINE)

_PLAIN_CHAPTER = re.compile(
    r"^\s*(chapter|part|appendix)\s+[\dIVXLCivxlc]+\b.*$", re.MULTILINE
)
_CN_CHAPTER = re.compile(r"^\s*第[0-9一二三四五六七八九十百千]+[章回节]\s*.*$", re.MULTILINE)

_MD_FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _headings(text: str) -> List[Tuple[int, str, int]]:
    out = []
    for m in _MD_HEADING.finditer(text):
        out.append((len(m.group(1)), m.group(2).strip(), m.start()))
    return out


def detect_chapters(text: str, fmt: str) -> List[Chapter]:
    if fmt == "md":
        chapters = _md_chapters(text)
        if len(chapters) >= 2:
            return chapters
    chapters = _plain_chapters(text)
    if len(chapters) >= 2:
        return chapters
    if fmt == "md":
        # fall through md with too few headings to plain patterns first,
        # already tried; go synthetic
        pass
    return _synthetic_chapters(text)


def _mk_chapters(text: str, marks: List[Tuple[int, str, int]], level: int) -> List[Chapter]:
    chapters = []
    for i, (lvl, title, start) in enumerate(marks):
        end = marks[i + 1][2] if i + 1 < len(marks) else len(text)
        chapters.append(
            Chapter(index=i + 1, title=title, start=start, end=end, level=level)
        )
    return chapters


def _md_chapters(text: str) -> List[Chapter]:
    headings = [h for h in _headings(text) if h[0] <= 3]
    if len(headings) < 2:
        return []
    counts: dict = {}
    for lvl, _, _ in headings:
        counts[lvl] = counts.get(lvl, 0) + 1
    # choose the densest heading level; ties -> shallower level
    best = min(counts.items(), key=lambda kv: (-kv[1], kv[0]))[0]
    marks = [h for h in headings if h[0] == best]
    if len(marks) < 2:
        return []
    return _mk_chapters(text, marks, best)


def _plain_chapters(text: str) -> List[Chapter]:
    marks: List[Tuple[int, str, int]] = []
    for m in _PLAIN_CHAPTER.finditer(text):
        marks.append((0, m.group(0).strip(), m.start()))
    for m in _CN_CHAPTER.finditer(text):
        marks.append((0, m.group(0).strip(), m.start()))
    marks.sort(key=lambda t: t[2])
    # dedupe overlapping
    dedup: List[Tuple[int, str, int]] = []
    for mark in marks:
        if dedup and mark[2] - dedup[-1][2] < 10:
            continue
        dedup.append(mark)
    if len(dedup) < 2:
        return []
    return _mk_chapters(text, dedup, 0)


def _synthetic_chapters(text: str) -> List[Chapter]:
    words = text.split()
    if not words:
        return []  # empty text (e.g. scanned pdf flagged for OCR): no chapters
    n = max(3, min(12, len(words) // 1200)) if len(words) > 1200 else 3
    n = min(n, len(words))
    per = len(words) // n or 1
    chapters: List[Chapter] = []
    for i in range(n):
        start_word = i * per
        end_word = (i + 1) * per if i < n - 1 else len(words)
        start = len(" ".join(words[:start_word])) + (1 if start_word else 0)
        end = len(" ".join(words[:end_word]))
        chapters.append(
            Chapter(
                index=i + 1,
                title=f"Part {i + 1} of {n} (synthetic chunk)",
                start=min(start, len(text)),
                end=min(end, len(text)),
                level=0,
                synthetic=True,
            )
        )
    return chapters


def detect_meta(text: str, fmt: str) -> Tuple[Optional[str], Optional[str]]:
    """Best-effort (title, author) hints."""
    fm = _MD_FRONTMATTER.match(text)
    if fm:
        try:
            import yaml

            meta = yaml.safe_load(fm.group(1)) or {}
            title = meta.get("title")
            author = meta.get("author")
            if title or author:
                return (title, author)
        except Exception:
            pass
    for lvl, title, _ in _headings(text):
        if lvl == 1 and len(title) < 100:
            return (title, None)
        break
    for line in text.splitlines():
        line = line.strip()
        if line and len(line) < 100:
            return (line, None)
    return (None, None)
