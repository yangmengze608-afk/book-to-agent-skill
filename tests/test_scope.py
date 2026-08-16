"""Book-only scope gate regression tests."""

from pathlib import Path

from book_to_agent_skill.models import Book
from book_to_agent_skill.scope import assess_document_scope


def _book(text: str) -> Book:
    return Book(
        path=Path("sample.pdf"),
        fmt="pdf",
        text=text,
        chapters=[],
        title_hint="Sample",
        author_hint="Author",
        ocr_required=False,
    )


def test_research_article_is_rejected():
    text = """DOI: 10.1002/example.12345
ORIGINAL PAPER
A Controlled Experiment About Training

Abstract
We tested a training intervention.

1 | INTRODUCTION
Background.

2 | MATERIALS AND METHODS
Participants were randomized.

3 | RESULTS
The intervention changed the outcome.

4 | DISCUSSION
The findings support the hypothesis.

5 | CONCLUSION
The effect was task specific.

CONFLICT OF INTEREST STATEMENT
None.
DATA AVAILABILITY STATEMENT
Data are available on request.
"""
    result = assess_document_scope(_book(text))
    assert not result.in_scope
    assert result.kind == "research-article"
    assert result.confidence >= 0.8
    assert "DOI near document start" in result.evidence
    assert "formal methods section" in result.evidence
    assert "formal results section" in result.evidence


def test_book_with_generic_headings_is_not_false_positive():
    text = """# The Craft of Decisions

## Introduction
This book explains practical decision habits. It discusses results from
several examples, but it is not a journal article.

## Principles
Start by defining the decision before collecting evidence.

## Methods for Better Thinking
This is an informal chapter title, not an IMRaD research report.

## Conclusion
Review the process after the outcome is known.
"""
    result = assess_document_scope(_book(text))
    assert result.in_scope
    assert result.kind == "book-or-unknown"


def test_cli_init_rejects_obvious_article_before_workspace(tmp_path, capsys):
    from book_to_agent_skill.cli import main

    article = tmp_path / "paper.txt"
    article.write_text(
        """DOI: 10.1234/example.1
RESEARCH ARTICLE
Abstract
Study summary.

1 | METHODS
Procedure.

2 | RESULTS
Findings.

3 | DISCUSSION
Interpretation.

4 | CONCLUSION
Conclusion.

DATA AVAILABILITY STATEMENT
Available on request.
""",
        encoding="utf-8",
    )
    workspace = tmp_path / "ws"
    rc = main(["init", str(article), "--workspace", str(workspace)])
    out = capsys.readouterr().out

    assert rc == 2
    assert "out of scope" in out.lower()
    assert "research-article" in out
    assert not workspace.exists()
