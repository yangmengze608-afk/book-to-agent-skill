"""CLI entry point: book2skill / python -m book_to_agent_skill"""

import argparse
import os
import shutil
import sys
from pathlib import Path

from . import __version__
from .classify import heuristic_classify, validate_classification
from .distill import (
    apply_provider_result,
    distill_request,
    distillation_workorder,
    scaffold_skill_dir,
)
from .evalgen import check_eval_cases, eval_context, eval_workorder
from .ingest import IngestError, ingest
from .models import Book
from .providers import get_provider
from .providers.base import NeedsAgentReasoning, ProviderError
from .taxonomy import Taxonomy, TaxonomyError
from .util import read_text, read_yaml, slugify, write_text, write_yaml
from .validate import SkillValidator
from .workspace import Workspace

COMMANDS = ["run", "init", "distill", "validate", "finalize", "doctor"]


# --------------------------------------------------------------------- helpers

def _print_classification(taxonomy: Taxonomy, cls: dict) -> None:
    label = taxonomy.label(cls["primary_category"])
    sub = cls.get("subcategory")
    print("Classification:")
    print(
        f"  {label}"
        + (f" -> {sub}" if sub else "")
        + f" (confidence {cls['confidence']}, method {cls['method']})"
    )
    for alt in cls.get("alternative_categories", []):
        print(f"  alternative: {alt['category']} ({alt['confidence']})")


def _init_workspace(ws: Workspace, book: Book, taxonomy: Taxonomy) -> dict:
    ws.ensure()
    write_text(ws.book_text, book.text)
    write_yaml(ws.source_meta, book.source_meta.to_dict())
    write_yaml(
        ws.structure,
        {
            "title_hint": book.title_hint,
            "author_hint": book.author_hint,
            "chapters": [
                {
                    "index": c.index,
                    "title": c.title,
                    "start": c.start,
                    "end": c.end,
                    "level": c.level,
                    "synthetic": c.synthetic,
                    "words": c.words(book.text),
                }
                for c in book.chapters
            ],
        },
    )
    heuristic = heuristic_classify(book, taxonomy).to_dict()
    if not ws.load_classification():
        write_yaml(ws.classification, heuristic)
    write_text(
        ws.classification_workorder,
        _classification_wo_text(book, taxonomy, heuristic),
    )
    ws.save_state(
        book_path=str(book.path),
        slug=slugify(book.title_hint or book.path.stem),
        phase="classification",
        classification_method=heuristic["method"],
    )
    return heuristic


def _classification_wo_text(book, taxonomy, heuristic):
    from .distill import classification_workorder

    return classification_workorder(book, taxonomy, heuristic)


def _load_book_for_workspace(ws: Workspace) -> Book:
    state = ws.load_state()
    book_path = state.get("book_path")
    if not book_path or not Path(book_path).exists():
        # fall back to re-ingesting from workspace text (structure already saved)
        if not ws.book_text.exists():
            raise IngestError(
                f"workspace {ws.root} has no book text; run `book2skill init` first"
            )
    if book_path and Path(book_path).exists():
        book = ingest(Path(book_path))
    else:
        raise IngestError(f"original book missing ({book_path}); re-run init")
    return book


# --------------------------------------------------------------------- commands

def cmd_init(args) -> int:
    taxonomy = Taxonomy()
    if taxonomy.validate():
        print("taxonomy errors:\n" + "\n".join(taxonomy.validate()))
        return 2
    book = ingest(Path(args.book))
    if book.ocr_required:
        print(
            f"OCR required: '{book.path.name}' looks like a scanned PDF "
            "(no text layer). V1 does not do OCR - see README Limitations."
        )
        return 2
    ws = Workspace(Path(args.workspace)).ensure()
    _init_workspace(ws, book, taxonomy)
    print(f"Book: {book.title_hint or book.path.name} ({book.fmt}, "
          f"{len(book.chapters)} chapters, ~{book.words} words)")
    heuristic = heuristic_classify(book, taxonomy)
    _print_classification(taxonomy, heuristic.to_dict())
    print(f"Workspace ready: {ws.root}")
    print("Next: review classification (workorder/01-classification.md), "
          "then `book2skill distill --workspace ...`")
    return 0


def cmd_distill(args) -> int:
    taxonomy = Taxonomy()
    ws = Workspace(Path(args.workspace))
    cls = ws.load_classification()
    if not cls:
        print(f"no classification.yaml in {ws.root}; run init + classification first")
        return 2
    errors = validate_classification(cls, taxonomy)
    if errors:
        print("classification invalid:")
        for e in errors:
            print(f"  - {e}")
        return 2
    _print_classification(taxonomy, cls)

    book = _load_book_for_workspace(ws)
    skill_md = ws.skill_dir / "SKILL.md"
    if skill_md.exists() and "TODO" not in read_text(skill_md):
        if not args.force:
            print("skill/SKILL.md already filled in (refusing to overwrite; --force to re-scaffold)")
        else:
            scaffold_skill_dir(ws.skill_dir, book, cls, taxonomy)
    else:
        scaffold_skill_dir(ws.skill_dir, book, cls, taxonomy)

    write_text(ws.distill_workorder, distillation_workorder(book, cls, taxonomy))
    ws.save_state(phase="distillation", classification_method=cls.get("method"))
    print(f"Scaffold + work order written: {ws.skill_dir}")
    print("Next: fill skill/SKILL.md + references/ (workorder/02-distillation.md), "
          "then evals (workorder/03-evals.md), then finalize")
    return 0


def cmd_validate(args) -> int:
    try:
        validator = SkillValidator(Path(args.skill_dir))
    except TaxonomyError as e:
        print(str(e))
        return 2
    passed = validator.run()
    print(validator.report())
    print("Validation: " + ("PASS" if passed else "FAIL"))
    return 0 if passed else 2


def _install_skill(ws: Workspace, output_root: Path, overwrite: bool) -> Path:
    book_meta = read_yaml(ws.skill_dir / "BOOK.yaml") or {}
    category = book_meta.get("primary_category", "other")
    slug = book_meta.get("slug") or ws.skill_dir.name
    target = output_root / category / slug
    if target.exists() and not overwrite:
        raise SystemExit(
            f"duplicate skill target already exists: {target} "
            "(use --overwrite to replace)"
        )
    if target.exists():
        shutil.rmtree(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ws.skill_dir, target)
    return target


def cmd_finalize(args) -> int:
    ws = Workspace(Path(args.workspace))
    if not (ws.skill_dir / "SKILL.md").exists():
        print(f"no skill in {ws.skill_dir}; run distill first")
        return 2
    validator = SkillValidator(ws.skill_dir)
    passed = validator.run()
    print(validator.report())
    if not passed:
        print("Validation: FAIL - fix the issues above, then re-run finalize")
        return 2
    target = _install_skill(ws, Path(args.output), args.overwrite)
    cases = read_yaml(ws.skill_dir / "evals" / "cases.yaml") or []
    print(f"Output: {target}")
    print(f"Eval: {len(cases)}/{sum((5, 5, 5, 3))} minimum met - {len(cases)} cases generated")
    print("Validation: PASS")
    ws.save_state(phase="done", output=str(target))
    return 0


def cmd_run(args) -> int:
    taxonomy = Taxonomy()
    book_path = Path(args.book)
    slug = slugify(book_path.stem)
    ws = Workspace(Path(args.workspace) if args.workspace else
                   Path.cwd() / f"b2a-workspace-{slug}").ensure()
    try:
        book = ingest(book_path)
    except IngestError as e:
        print(str(e))
        return 2
    if book.ocr_required:
        print(f"OCR required: '{book.path.name}' looks like a scanned PDF. "
              "V1 does not do OCR - see README Limitations.")
        return 2

    print(f"Book: {book.title_hint or book_path.name} ({book.fmt}, "
          f"{len(book.chapters)} chapters, ~{book.words} words)")
    heuristic = _init_workspace(ws, book, taxonomy)

    provider_name = args.provider or os.environ.get("B2A_PROVIDER", "agent")
    provider = get_provider(provider_name)

    if provider.name in ("openai", "anthropic"):
        try:
            cls = provider.classify(book.digest(12000), taxonomy)
            errors = validate_classification(cls, taxonomy)
            if errors:
                print("provider classification invalid: " + "; ".join(errors))
                return 2
            write_yaml(ws.classification, cls)
            _print_classification(taxonomy, cls)
            print("Generating skill...")
            request = distill_request(book, cls, taxonomy)
            result = provider.distill(request)
            scaffold_skill_dir(ws.skill_dir, book, cls, taxonomy)
            apply_provider_result(ws.skill_dir, result, slug)
            skill_md = read_text(ws.skill_dir / "SKILL.md")
            cases = provider.evals(
                eval_context(book, cls, skill_md)
            )
            case_errors = check_eval_cases(cases, taxonomy.eval_minimums())
            if case_errors:
                print("provider evals invalid: " + "; ".join(case_errors[:4]))
                print("falling back to agent for evals (workorder/03-evals.md)")
                write_text(ws.eval_workorder, eval_workorder(book, cls, skill_md))
            else:
                write_yaml(ws.skill_dir / "evals" / "cases.yaml", cases)
            passed = SkillValidator(ws.skill_dir).run()
            if not passed:
                print("validation failed after provider generation; see `book2skill validate`")
                return 2
            target = _install_skill(ws, Path(args.output), args.overwrite)
            n = len(read_yaml(ws.skill_dir / "evals" / "cases.yaml") or [])
            print(f"Output: {target}")
            print(f"Eval: {n} cases generated")
            print("Validation: PASS")
            return 0
        except ProviderError as e:
            print(f"provider error: {e}")
            print("falling back to agent mode - work orders staged")
        except NeedsAgentReasoning as e:
            print(str(e))

    # agent / heuristic mode: deterministic steps + staged work orders
    _print_classification(taxonomy, heuristic)
    if provider.name == "heuristic":
        cls = heuristic
    else:
        cls = ws.load_classification() or heuristic
    scaffold_skill_dir(ws.skill_dir, book, cls, taxonomy)
    write_text(ws.distill_workorder, distillation_workorder(book, cls, taxonomy))
    skill_excerpt = read_text(ws.skill_dir / "SKILL.md")[:4000]
    write_text(ws.eval_workorder, eval_workorder(book, cls, skill_excerpt))
    ws.save_state(phase="distillation")
    print("Agent mode: reasoning stages staged as work orders:")
    print(f"  1. {ws.classification_workorder}")
    print(f"  2. {ws.distill_workorder}")
    print(f"  3. {ws.eval_workorder}")
    print("Fill them (or set OPENAI_API_KEY / ANTHROPIC_API_KEY and re-run "
          "with --provider), then `book2skill finalize --workspace ...`")
    return 0


def cmd_doctor(args) -> int:
    print(f"book-to-agent-skill {__version__}")
    errors = Taxonomy().validate()
    if errors:
        print("taxonomy errors:")
        for e in errors:
            print(f"  - {e}")
        return 2
    tax = Taxonomy()
    print(f"taxonomy: {len(tax.category_ids())} categories OK")
    provider = os.environ.get("B2A_PROVIDER", "agent")
    print(f"provider: {provider} (env B2A_PROVIDER)")
    print(f"openai key set: {bool(os.environ.get('OPENAI_API_KEY'))}")
    print(f"anthropic key set: {bool(os.environ.get('ANTHROPIC_API_KEY'))}")
    return 0


# ----------------------------------------------------------------------- main

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="book2skill",
        description="Turn a book into one reusable Agent Skill - "
                    "classify first, distill second.",
    )
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="command")

    run = sub.add_parser("run", help="full pipeline on one book")
    run.add_argument("book", help="path to .pdf/.epub/.txt/.md")
    run.add_argument("--workspace", help="workspace dir (default ./b2a-workspace-<slug>)")
    run.add_argument("--output", default="output", help="output root (default ./output)")
    run.add_argument("--provider", choices=["agent", "heuristic", "openai", "anthropic"],
                     help="reasoning provider (default $B2A_PROVIDER or agent)")
    run.add_argument("--overwrite", action="store_true", help="replace existing target")
    run.set_defaults(func=cmd_run)

    init = sub.add_parser("init", help="ingest + structure + classification staging")
    init.add_argument("book")
    init.add_argument("--workspace", required=True)
    init.set_defaults(func=cmd_init)

    distill = sub.add_parser("distill", help="validate classification + scaffold skill")
    distill.add_argument("--workspace", required=True)
    distill.add_argument("--force", action="store_true", help="re-scaffold a filled skill")
    distill.set_defaults(func=cmd_distill)

    validate = sub.add_parser("validate", help="validate a skill directory")
    validate.add_argument("skill_dir")
    validate.set_defaults(func=cmd_validate)

    finalize = sub.add_parser("finalize", help="validate + install skill to output/")
    finalize.add_argument("--workspace", required=True)
    finalize.add_argument("--output", default="output")
    finalize.add_argument("--overwrite", action="store_true")
    finalize.set_defaults(func=cmd_finalize)

    doctor = sub.add_parser("doctor", help="check taxonomy and environment")
    doctor.set_defaults(func=cmd_doctor)

    return p


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] not in COMMANDS and not argv[0].startswith("-"):
        if Path(argv[0]).exists():  # `book2skill ./book.pdf` -> run
            argv = ["run"] + argv
    args = build_parser().parse_args(argv)
    if not getattr(args, "command", None):
        build_parser().print_help()
        return 0
    try:
        return args.func(args)
    except (IngestError, TaxonomyError) as e:
        print(f"error: {e}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
