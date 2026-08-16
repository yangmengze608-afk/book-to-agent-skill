"""2/3/6/7. Skill validation: BOOK.yaml schema, required sections,
duplicate slug install, malformed metadata, eval counts."""

import shutil

import pytest
import yaml

from book_to_agent_skill.util import read_yaml, write_yaml
from book_to_agent_skill.validate import SkillValidator


def _copy_skill(example_skill, tmp_path):
    target = tmp_path / "the-decision-notebook"
    shutil.copytree(example_skill, target)
    return target


def test_example_skill_passes_validation(example_skill, taxonomy):
    validator = SkillValidator(example_skill, taxonomy)
    assert validator.run(), validator.report()


def test_generated_skill_has_required_sections(example_skill, taxonomy):
    """3. The generated skill must teach the book's method, not summarize
    it - enforced via the category profile's section list."""
    from book_to_agent_skill.skillfile import missing_sections, section_names

    skill_md = (example_skill / "SKILL.md").read_text(encoding="utf-8")
    profile = taxonomy.profile("decision-making")
    assert missing_sections(skill_md, profile["skill_sections"]) == []
    sections = {s.lower() for s in section_names(skill_md)}
    assert "purpose" in sections and "use when" in sections
    assert "final quality check" in sections
    # not a book report
    assert "chapter 1 summary" not in skill_md.lower()


def test_malformed_book_yaml_fails(example_skill, taxonomy, tmp_path):
    """7. Malformed metadata must be caught by the schema."""
    skill = _copy_skill(example_skill, tmp_path)
    meta = read_yaml(skill / "BOOK.yaml")
    del meta["primary_category"]  # required field removed
    write_yaml(skill / "BOOK.yaml", meta)
    validator = SkillValidator(skill, taxonomy)
    assert not validator.run()
    result = [r for r in validator.results if r.name == "book-yaml"]
    assert result and not result[0].ok


def test_book_yaml_unknown_category_fails(example_skill, taxonomy, tmp_path):
    skill = _copy_skill(example_skill, tmp_path)
    meta = read_yaml(skill / "BOOK.yaml")
    meta["primary_category"] = "not-a-category"
    write_yaml(skill / "BOOK.yaml", meta)
    validator = SkillValidator(skill, taxonomy)
    assert not validator.run()


def test_missing_section_fails(example_skill, taxonomy, tmp_path):
    skill = _copy_skill(example_skill, tmp_path)
    path = skill / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("## Failure Modes", "## Renamed Section")
    path.write_text(text, encoding="utf-8")
    validator = SkillValidator(skill, taxonomy)
    assert not validator.run()
    result = [r for r in validator.results if r.name == "skill-sections"]
    assert result and "Failure Modes" in result[0].detail


def test_todo_markers_fail(example_skill, taxonomy, tmp_path):
    skill = _copy_skill(example_skill, tmp_path)
    path = skill / "references" / "examples.md"
    path.write_text(path.read_text(encoding="utf-8") + "\nTODO fill me\n",
                    encoding="utf-8")
    validator = SkillValidator(skill, taxonomy)
    validator.run()
    result = [r for r in validator.results if r.name == "draft-complete"]
    assert result and not result[0].ok


def test_too_few_eval_cases_fail(example_skill, taxonomy, tmp_path):
    """Eval minimums: 5/5/5/3 by type."""
    skill = _copy_skill(example_skill, tmp_path)
    cases = read_yaml(skill / "evals" / "cases.yaml")
    # drop all but one edge case
    cases = [c for c in cases if c["type"] != "edge_case"] + [
        c for c in cases if c["type"] == "edge_case"
    ][:1]
    write_yaml(skill / "evals" / "cases.yaml", cases)
    validator = SkillValidator(skill, taxonomy)
    validator.run()
    result = [r for r in validator.results if r.name == "eval-cases"]
    assert result and not result[0].ok
    assert "edge_case" in result[0].detail


def test_duplicate_slug_install_refused(example_skill, tmp_path, capsys):
    """6. Finalize must refuse to overwrite an existing skill target
    without --overwrite."""
    from book_to_agent_skill.cli import _install_skill
    from book_to_agent_skill.workspace import Workspace

    ws = Workspace(tmp_path / "ws").ensure()
    shutil.copytree(example_skill, ws.skill_dir)
    # workspace BOOK.yaml keeps the canonical slug (dir is staged as 'skill')
    output = tmp_path / "output"
    first = _install_skill(ws, output, overwrite=False)
    assert (first / "SKILL.md").exists()
    with pytest.raises(SystemExit, match="duplicate"):
        _install_skill(ws, output, overwrite=False)
    # --overwrite replaces cleanly
    second = _install_skill(ws, output, overwrite=True)
    assert second == first and (second / "SKILL.md").exists()


def test_workspace_staging_name_mismatch_tolerated(example_skill, taxonomy, tmp_path):
    """A skill staged in a workspace dir literally named 'skill' must
    validate against its BOOK.yaml slug, not the directory name."""
    skill = _copy_skill(example_skill, tmp_path / "ws")
    staged = tmp_path / "ws" / "skill"
    skill.rename(staged)
    validator = SkillValidator(staged, taxonomy)
    assert validator.run(), validator.report()
