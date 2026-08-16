"""Classification: heuristic pre-classifier + validation.

The heuristic is deliberately conservative: it produces a low-confidence
hint that an agent (or an API provider) is expected to confirm or replace.
"""

import json
import re
from typing import List

import jsonschema

from .models import Book, Classification
from .paths import schemas_dir
from .taxonomy import Taxonomy

HEURISTIC_CONFIDENCE_CAP = 0.6
BOOK_TYPES = {
    "monograph",
    "textbook",
    "handbook",
    "essay-collection",
    "biography",
    "narrative",
    "other",
}


def _schema(name: str) -> dict:
    return json.loads((schemas_dir() / name).read_text(encoding="utf-8"))


# ------------------------------------------------------------- book metadata

def detect_language(text: str) -> str:
    """Return a conservative ISO-like language hint.

    V1 intentionally recognizes only languages that can be detected with high
    confidence from script alone. Everything else is ``und`` (undetermined)
    rather than a fabricated guess.
    """
    sample = (text or "")[:50000]
    if not sample.strip():
        return "und"

    kana = len(re.findall(r"[\u3040-\u30ff]", sample))
    hangul = len(re.findall(r"[\uac00-\ud7af]", sample))
    cjk = len(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]", sample))
    latin = len(re.findall(r"[A-Za-z]", sample))

    if kana >= 10:
        return "ja"
    if hangul >= 10:
        return "ko"
    # Chinese texts often contain English terms; require meaningful CJK signal
    # rather than a majority of all alphabetic characters.
    if cjk >= 20 and cjk >= latin * 0.20:
        return "zh"
    if latin >= 20:
        return "en"
    return "und"


def infer_book_type(book: Book) -> str:
    """Infer book type only when there is an explicit structural signal.

    The fallback is ``other`` instead of pretending every book is a monograph.
    The reasoning agent should replace this hint when it can identify the type
    from the whole book.
    """
    title = (book.title_hint or book.path.stem or "").lower()
    chapter_titles = " ".join(book.chapter_titles()).lower()
    combined = f"{title} {chapter_titles}"

    if re.search(r"\b(textbook|coursebook|workbook)\b", combined):
        return "textbook"
    if re.search(r"\b(handbook|manual|reference guide)\b", combined):
        return "handbook"
    if re.search(r"\b(autobiography|biography|memoir|life of)\b", combined):
        return "biography"
    if re.search(r"\b(collected essays|selected essays|essays)\b", combined):
        return "essay-collection"
    if re.search(r"\b(novel|short stories|stories|fiction)\b", combined):
        return "narrative"

    # Exercise/problem-set heavy structures are a useful textbook signal even
    # when the title itself does not contain "textbook".
    if book.chapters:
        exercise_like = sum(
            1
            for c in book.chapters
            if re.search(r"\b(exercises?|problem sets?|review questions?)\b", c.title.lower())
        )
        if len(book.chapters) >= 4 and exercise_like / len(book.chapters) >= 0.25:
            return "textbook"

    return "other"


# ---------------------------------------------------------------- heuristic

def _count_keyword(haystack: str, keyword: str) -> int:
    if not keyword:
        return 0
    pattern = (
        rf"\b{re.escape(keyword.lower())}\b"
        if " " not in keyword.strip() and "-" not in keyword
        else re.escape(keyword.lower())
    )
    return len(re.findall(pattern, haystack))


def heuristic_classify(book: Book, taxonomy: Taxonomy) -> Classification:
    title = (book.title_hint or "").lower()
    chapter_titles = " ".join(book.chapter_titles()).lower()

    body_parts = []
    for ch in book.chapters:
        body = ch.body(book.text)
        if not body:
            continue
        body_parts.append(body[:2000].lower())
        body_parts.append(body[len(body) // 2 : len(body) // 2 + 1500].lower())
    body = " ".join(body_parts)

    language = detect_language(book.text)
    book_type = infer_book_type(book)

    scores = {}
    for cat in taxonomy.categories:
        score = 0.0
        for kw in cat.get("keywords", []):
            k = kw.lower().strip()
            if not k:
                continue
            score += 6.0 * _count_keyword(title, k)
            score += 3.0 * _count_keyword(chapter_titles, k)
            score += 1.0 * _count_keyword(body, k)
        scores[cat["id"]] = score

    ranked = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
    top_id, top_score = ranked[0]
    second_id, second_score = ranked[1] if len(ranked) > 1 else (None, 0.0)

    if top_score <= 0 or top_id == "other" and second_score <= 0:
        return Classification(
            primary_category="other",
            confidence=0.15,
            rationale=(
                "Keyword heuristic found no meaningful signal in the book's "
                "title, chapter titles, or sampled body text. An agent must "
                "classify this book by reading the digest."
            ),
            method="heuristic",
            tags=[],
            language=language,
            book_type=book_type,
        )

    share = top_score / (top_score + max(second_score, 1.0))
    confidence = round(min(HEURISTIC_CONFIDENCE_CAP, 0.3 + 0.3 * share), 2)
    alternatives = [
        {"category": second_id, "confidence": round(confidence * 0.7, 2)}
    ] if second_id and second_score > 0 else []

    return Classification(
        primary_category=top_id,
        confidence=confidence,
        rationale=(
            f"Keyword heuristic matched '{taxonomy.label(top_id)}' most strongly "
            f"(score {top_score:.0f} vs runner-up {second_id} at {second_score:.0f}) "
            f"across title, chapter titles, and sampled body text. This is a "
            f"hint only: method=heuristic, confidence capped at "
            f"{HEURISTIC_CONFIDENCE_CAP}; an agent should confirm or replace it."
        ),
        method="heuristic",
        alternative_categories=alternatives,
        tags=[],
        language=language,
        book_type=book_type,
    )


# --------------------------------------------------------------- validation

def validate_classification(data: dict, taxonomy: Taxonomy) -> List[str]:
    """Schema + taxonomy cross-checks. Returns a list of error strings."""
    errors: List[str] = []
    try:
        jsonschema.validate(data, _schema("classification.schema.json"))
    except jsonschema.ValidationError as e:
        return [f"classification schema: {e.message}"]

    primary = data["primary_category"]
    if primary not in taxonomy.by_id:
        errors.append(
            f"unknown primary_category '{primary}' "
            f"(valid: {', '.join(taxonomy.category_ids())})"
        )
        return errors

    sub = data.get("subcategory")
    allowed = taxonomy.by_id[primary].get("subcategories", [])
    if sub and allowed and sub not in allowed and sub != "general":
        errors.append(
            f"subcategory '{sub}' not in {primary}'s list {allowed}"
        )

    if data["method"] == "heuristic" and data["confidence"] > HEURISTIC_CONFIDENCE_CAP:
        errors.append(
            f"heuristic classification confidence {data['confidence']} exceeds "
            f"cap {HEURISTIC_CONFIDENCE_CAP}"
        )

    for alt in data.get("alternative_categories", []):
        if alt["category"] not in taxonomy.by_id:
            errors.append(f"unknown alternative category '{alt['category']}'")

    return errors
