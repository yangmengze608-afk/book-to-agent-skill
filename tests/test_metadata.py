"""Book metadata must be inferred conservatively instead of hard-coded."""

from pathlib import Path

from book_to_agent_skill.classify import detect_language, infer_book_type
from book_to_agent_skill.distill import build_book_yaml
from book_to_agent_skill.models import Book, Chapter, SourceMeta


def _book(text: str, title: str = "A Book", chapter_titles=None) -> Book:
    chapter_titles = chapter_titles or ["Chapter 1"]
    chapters = []
    # Tests only need titles for metadata inference; sharing the same text span
    # keeps the fixture deliberately small.
    for i, chapter_title in enumerate(chapter_titles, start=1):
        chapters.append(
            Chapter(
                index=i,
                title=chapter_title,
                start=0,
                end=len(text),
                level=1,
                synthetic=False,
            )
        )
    source_meta = SourceMeta(
        original_path="/tmp/book.md",
        format="md",
        sha256="a" * 64,
        word_count=max(1, len(text.split())),
        chapter_count=len(chapters),
        ocr_required=False,
    )
    return Book(
        path=Path("/tmp/book.md"),
        fmt="md",
        text=text,
        chapters=chapters,
        title_hint=title,
        author_hint="Test Author",
        ocr_required=False,
        source_meta=source_meta,
    )


def test_detect_language_english():
    assert detect_language("Decision quality depends on evidence and uncertainty. " * 20) == "en"


def test_detect_language_chinese():
    text = "这是一本讨论决策、证据、不确定性和判断方法的中文书。" * 30
    assert detect_language(text) == "zh"


def test_detect_language_japanese_before_cjk_fallback():
    text = "これは意思決定についての本です。判断と証拠を検討します。" * 30
    assert detect_language(text) == "ja"


def test_infer_explicit_handbook_type():
    book = _book("Some content " * 100, title="The Practical Research Handbook")
    assert infer_book_type(book) == "handbook"


def test_infer_unknown_type_does_not_pretend_monograph():
    book = _book("Some content " * 100, title="Thinking Clearly")
    assert infer_book_type(book) == "other"


def test_build_book_yaml_prefers_agent_metadata():
    book = _book("这是一本中文书。" * 50)
    cls = {
        "primary_category": "decision-making",
        "confidence": 0.9,
        "tags": [],
        "language": "zh",
        "book_type": "textbook",
    }
    meta = build_book_yaml(book, cls, "test-book")
    assert meta["language"] == "zh"
    assert meta["book_type"] == "textbook"


def test_build_book_yaml_falls_back_conservatively_for_old_classification():
    book = _book("这是一本讨论如何做决定的中文书。" * 50, title="Decision Notes")
    cls = {
        "primary_category": "decision-making",
        "confidence": 0.8,
        "tags": [],
    }
    meta = build_book_yaml(book, cls, "decision-notes")
    assert meta["language"] == "zh"
    assert meta["book_type"] == "other"
