"""Core data model shared across pipeline stages."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from .util import clean_excerpt, word_count


@dataclass
class Chapter:
    index: int  # 1-based
    title: str
    start: int  # char offset into Book.text
    end: int
    level: int  # heading level; 0 for synthetic chunks
    synthetic: bool = False

    def body(self, text: str) -> str:
        return text[self.start : self.end]

    def words(self, text: str) -> int:
        return word_count(self.body(text))


@dataclass
class SourceMeta:
    original_path: str
    format: str
    sha256: str
    word_count: int
    chapter_count: int
    ocr_required: bool
    notes: str = ""

    def to_dict(self) -> dict:
        return {
            "original_path": self.original_path,
            "sha256": self.sha256,
            "word_count": self.word_count,
            "chapter_count": self.chapter_count,
            "ocr_required": self.ocr_required,
            "notes": self.notes,
        }


@dataclass
class Book:
    path: Path
    fmt: str  # pdf | epub | txt | md
    text: str
    chapters: List[Chapter]
    title_hint: str
    author_hint: str
    ocr_required: bool
    source_meta: SourceMeta = field(default=None)  # type: ignore[assignment]

    @property
    def words(self) -> int:
        return word_count(self.text)

    def chapter_titles(self) -> List[str]:
        return [c.title for c in self.chapters]

    def digest(self, max_chars: int = 14000) -> str:
        """A compact, structured digest for classification / distillation."""
        lines: List[str] = []
        lines.append(f"TITLE: {self.title_hint or '(unknown)'}")
        lines.append(f"AUTHOR: {self.author_hint or '(unknown)'}")
        lines.append(f"FORMAT: {self.fmt}")
        lines.append(f"WORDS: {self.words}")
        lines.append(f"CHAPTERS: {len(self.chapters)}")
        lines.append("")
        lines.append("CHAPTER TITLES:")
        for c in self.chapters:
            marker = " [synthetic]" if c.synthetic else ""
            lines.append(f"  {c.index}. {c.title} (~{c.words(self.text)} words){marker}")
        lines.append("")
        lines.append("EXCERPTS:")
        # Per-chapter excerpts: beginning + a middle sample, budgeted.
        budget = max(600, (max_chars - 600) // max(1, len(self.chapters)))
        for c in self.chapters:
            body = c.body(self.text)
            head = clean_excerpt(body[: max(200, budget * 2 // 3)], budget * 2 // 3)
            mid_start = max(0, len(body) // 2)
            mid = clean_excerpt(body[mid_start : mid_start + budget // 3], budget // 3)
            excerpt = head if head == mid else (head + " ... " + mid)
            lines.append(f"--- [{c.index}] {c.title} ---")
            lines.append(excerpt)
        digest = "\n".join(lines)
        if len(digest) > max_chars:
            digest = digest[:max_chars] + "\n...[truncated]"
        return digest


@dataclass
class Classification:
    primary_category: str
    confidence: float
    rationale: str
    method: str  # heuristic | agent | openai | anthropic
    subcategory: Optional[str] = None
    alternative_categories: List[dict] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        d = {
            "primary_category": self.primary_category,
            "subcategory": self.subcategory,
            "confidence": self.confidence,
            "rationale": self.rationale,
            "alternative_categories": self.alternative_categories,
            "tags": self.tags,
            "method": self.method,
        }
        return {k: v for k, v in d.items() if v is not None}
