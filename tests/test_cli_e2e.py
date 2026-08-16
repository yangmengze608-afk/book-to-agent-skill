"""End-to-end: the full pipeline on the example book (agent/heuristic mode).

Verifies the acceptance path: read book -> classify with rationale +
confidence -> category-specific strategy -> one skill scaffold + evals
staged -> workspace state machine advances.
"""

import yaml

from book_to_agent_skill.cli import main


def test_full_run_heuristic(example_book, tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    rc = main([
        "run", str(example_book),
        "--workspace", str(tmp_path / "ws"),
        "--provider", "heuristic",
    ])
    out = capsys.readouterr().out
    assert rc == 0, out

    ws = tmp_path / "ws"
    # staged reasoning artifacts
    assert (ws / "book" / "text.md").exists()
    assert (ws / "book" / "structure.yaml").exists()
    assert (ws / "classification.yaml").exists()
    assert (ws / "workorder" / "01-classification.md").exists()
    assert (ws / "workorder" / "02-distillation.md").exists()
    assert (ws / "workorder" / "03-evals.md").exists()

    cls = yaml.safe_load((ws / "classification.yaml").read_text(encoding="utf-8"))
    assert cls["primary_category"]
    assert 0 < cls["confidence"] <= 0.6  # heuristic cap: honest uncertainty
    assert cls["rationale"]

    # one skill scaffold (exactly one - never split per chapter)
    skill = ws / "skill"
    assert (skill / "SKILL.md").exists()
    assert (skill / "evals" / "cases.yaml").exists()
    refs = sorted(p.name for p in (skill / "references").iterdir())
    assert refs == [
        "examples.md", "frameworks.md", "limitations.md",
        "principles.md", "procedures.md", "source-map.md",
    ]

    # distillation work order embeds the category-specific strategy
    wo = (ws / "workorder" / "02-distillation.md").read_text(encoding="utf-8")
    assert cls["primary_category"] in wo

    # state machine advanced
    state = yaml.safe_load((ws / "state.yaml").read_text(encoding="utf-8"))
    assert state["phase"] == "distillation"
    assert "Classification:" in out


def test_doctor(capsys):
    assert main(["doctor"]) == 0
    out = capsys.readouterr().out
    assert "categories OK" in out
