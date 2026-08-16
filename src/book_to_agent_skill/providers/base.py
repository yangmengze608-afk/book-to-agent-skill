"""Provider interface + shared errors."""

from abc import ABC, abstractmethod


class NeedsAgentReasoning(Exception):
    """No API provider configured/fitted for this step.

    The pipeline catches this, writes a work order into the workspace, and
    instructs the caller (the agent following SKILL.md) to do the reasoning.
    """

    def __init__(self, stage: str, message: str = ""):
        self.stage = stage
        super().__init__(message or f"stage '{stage}' requires agent reasoning")


class ProviderError(Exception):
    """Configuration or API failure in a reasoning provider."""


class ReasoningProvider(ABC):
    """The three reasoning steps of the pipeline.

    - classify:   book digest  -> classification dict
    - distill:    request      -> {"skill_md": str, "references": {name: md}}
    - evals:      context      -> list of eval case dicts
    """

    name: str = "base"

    @abstractmethod
    def classify(self, book_digest: str, taxonomy) -> dict:
        ...

    @abstractmethod
    def distill(self, request: dict) -> dict:
        ...

    @abstractmethod
    def evals(self, context: dict) -> list:
        ...
