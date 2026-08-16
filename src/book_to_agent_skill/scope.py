"""Conservative scope checks for the book-only V1 pipeline.

The meta-skill deliberately targets one book at a time. File extensions alone
cannot distinguish a book PDF from a journal article, so this module applies a
high-precision detector for obvious scholarly articles before classification.

The detector is intentionally conservative: uncertain documents remain in
scope and are left to the agent's judgment. Only documents with several
independent article signals are rejected automatically.
"""

from dataclasses import dataclass, field
import re
from typing import List

from .models import Book


@dataclass(frozen=True)
class ScopeAssessment:
    in_scope: bool
    kind: str
    confidence: float
    evidence: List[str] = field(default_factory=list)
    reason: str = ""


_DOI_RE = re.compile(r"\bdoi\s*:\s*10\.\d{4,9}/\S+", re.IGNORECASE)
_ARTICLE_LABEL_RE = re.compile(
    r"\b(?:original paper|original article|research article|review article|"
    r"systematic review|meta[- ]analysis|brief report|short communication)\b",
    re.IGNORECASE,
)

# Section headings are intentionally anchored to lines so references to words
# such as "results" in prose do not inflate the score.
_SECTION_PATTERNS = {
    "abstract": re.compile(r"(?mi)^\s*abstract\s*$"),
    "methods": re.compile(
        r"(?mi)^\s*(?:\d+(?:\.\d+)?\s*[|.:\-]?\s*)?"
        r"(?:materials\s+and\s+methods|methods|methodology)\s*$"
    ),
    "results": re.compile(
        r"(?mi)^\s*(?:\d+(?:\.\d+)?\s*[|.:\-]?\s*)?results\s*$"
    ),
    "discussion": re.compile(
        r"(?mi)^\s*(?:\d+(?:\.\d+)?\s*[|.:\-]?\s*)?discussion\s*$"
    ),
    "conclusion": re.compile(
        r"(?mi)^\s*(?:\d+(?:\.\d+)?\s*[|.:\-]?\s*)?conclusions?\s*$"
    ),
}

_END_MATTER_RE = re.compile(
    r"(?mi)^\s*(?:conflict of interest(?: statement)?|data availability(?: statement)?|"
    r"ethics approval(?: statement)?|informed consent(?: statement)?)\s*$"
)


def assess_document_scope(book: Book) -> ScopeAssessment:
    """Return a conservative book-vs-obvious-article scope assessment.

    A positive article decision requires multiple independent signals. This is
    not a general document classifier and should not be expanded into one in
    V1; ambiguous inputs remain eligible for agent review.
    """

    text = book.text or ""
    head = text[:16000]
    score = 0.0
    evidence: List[str] = []

    if _DOI_RE.search(head):
        score += 2.0
        evidence.append("DOI near document start")

    if _ARTICLE_LABEL_RE.search(head):
        score += 3.0
        evidence.append("explicit scholarly article label")

    section_weights = {
        "abstract": 1.5,
        "methods": 1.5,
        "results": 1.5,
        "discussion": 1.5,
        "conclusion": 1.0,
    }
    for name, pattern in _SECTION_PATTERNS.items():
        # Search the whole document for formal section headings; the detector
        # still needs DOI/article-label corroboration or several headings.
        if pattern.search(text):
            score += section_weights[name]
            evidence.append(f"formal {name} section")

    if _END_MATTER_RE.search(text):
        score += 1.0
        evidence.append("journal-style research end matter")

    # High precision threshold: a book with a Conclusion and References should
    # never be rejected just for those headings. Typical research papers clear
    # this threshold comfortably through DOI/label + IMRaD structure.
    if score >= 7.0:
        confidence = min(0.99, round(0.72 + (score - 7.0) * 0.035, 2))
        return ScopeAssessment(
            in_scope=False,
            kind="research-article",
            confidence=confidence,
            evidence=evidence,
            reason=(
                "Input strongly matches a scholarly article rather than a book. "
                "book-to-agent-skill V1 is intentionally book-only."
            ),
        )

    return ScopeAssessment(
        in_scope=True,
        kind="book-or-unknown",
        confidence=round(max(0.2, 1.0 - score / 10.0), 2),
        evidence=evidence,
        reason=(
            "No high-confidence non-book pattern detected; leave final scope "
            "judgment to the agent."
        ),
    )


def enforce_book_scope(book: Book) -> ScopeAssessment:
    """Raise a clear error for obvious non-book inputs."""
    assessment = assess_document_scope(book)
    if not assessment.in_scope:
        evidence = "; ".join(assessment.evidence[:6])
        raise ValueError(
            f"out of scope: input appears to be a {assessment.kind} "
            f"(confidence {assessment.confidence}). {assessment.reason} "
            f"Evidence: {evidence}."
        )
    return assessment
