# Real-world scope benchmarks

These cases test a boundary that synthetic book examples cannot: a `.pdf` is
not necessarily a book. V1 is intentionally **one book → one skill**, so
obvious scholarly articles should stop before classification rather than be
forced through the book distillation pipeline.

No source PDFs or copyrighted article text are stored in this repository.
Only bibliographic metadata and the expected scope decision are recorded.

## Case 001 — Pechlivanos et al. (2024)

- **Title:** *Effects of plyometric training techniques on vertical jump performance of basketball players*
- **Venue:** European Journal of Sport Science, 24, 682–692
- **DOI:** `10.1002/ejsc.12097`
- **Input format:** PDF with extractable text
- **Expected scope decision:** `REJECT`
- **Expected kind:** `research-article`
- **Reason:** the document presents multiple independent scholarly-article signals: DOI near the start, an explicit `ORIGINAL PAPER` label, formal Abstract / Materials and Methods / Results / Discussion / Conclusion sections, and journal-style research end matter.
- **Observed detector score during the benchmark:** `13.0`
- **Observed confidence:** `0.93`
- **Regression requirement:** `book2skill init` / `book2skill run` must stop before creating a classification workspace for this class of input.

### Why this case matters

Before this benchmark, the root `SKILL.md` said articles were out of scope, but
the deterministic CLI only checked file format and OCR availability. A journal
article PDF could therefore continue into book classification and distillation.
This benchmark exposed that mismatch and led to the V1.1 scope gate.
