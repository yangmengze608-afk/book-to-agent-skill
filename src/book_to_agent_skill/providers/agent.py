"""AgentProvider (default): no API calls.

Every reasoning stage raises NeedsAgentReasoning; the pipeline stages the
work as markdown work orders inside the workspace for the calling agent
to execute per the root SKILL.md.
"""

from .base import NeedsAgentReasoning, ReasoningProvider


class AgentProvider(ReasoningProvider):
    name = "agent"

    def classify(self, book_digest: str, taxonomy) -> dict:
        raise NeedsAgentReasoning(
            "classification",
            "No reasoning provider configured. Read "
            "workorder/01-classification.md and write classification.yaml.",
        )

    def distill(self, request: dict) -> dict:
        raise NeedsAgentReasoning(
            "distillation",
            "No reasoning provider configured. Follow "
            "workorder/02-distillation.md, then fill skill/SKILL.md and "
            "skill/references/.",
        )

    def evals(self, context: dict) -> list:
        raise NeedsAgentReasoning(
            "evals",
            "No reasoning provider configured. Follow workorder/03-evals.md "
            "and fill skill/evals/cases.yaml.",
        )
