"""RRC decision agent using LLM."""

from typing import Any


class RRCDecisionAgent:
    """Generate RRC messages with explanations."""

    def __init__(self, model: Any) -> None:
        self.model = model

    def generate(self, prompt: str) -> str:
        """Call the LLM with the given prompt."""
        # TODO: Integrate with OpenAI or other LLM
        raise NotImplementedError
