"""HeuristicProvider: deterministic keyword classification, staged distillation.

Classification uses classify.heuristic_classify (confidence capped at 0.6
and method='heuristic' - it is a hint, never a verdict). Distillation and
eval generation still require agent reasoning.
"""

from ..classify import heuristic_classify
from ..models import Book
from .base import NeedsAgentReasoning, ReasoningProvider


class HeuristicProvider(ReasoningProvider):
    name = "heuristic"

    def classify(self, book_digest: str, taxonomy, book: Book = None) -> dict:
        if book is None:
            raise NeedsAgentReasoning(
                "classification", "heuristic provider needs the Book object"
            )
        return heuristic_classify(book, taxonomy).to_dict()

    def distill(self, request: dict) -> dict:
        raise NeedsAgentReasoning(
            "distillation",
            "heuristic provider cannot distill knowledge; use agent or an "
            "API provider for this stage",
        )

    def evals(self, context: dict) -> list:
        raise NeedsAgentReasoning(
            "evals",
            "heuristic provider cannot author eval cases; use agent or an "
            "API provider for this stage",
        )
