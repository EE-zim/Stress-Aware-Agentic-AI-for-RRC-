"""Tests for agent modules."""

from agents.network_context import NetworkContextAgent
from agents.rrc_decision import RRCDecisionAgent


def test_network_context_agent() -> None:
    """Placeholder test for NetworkContextAgent."""
    agent = NetworkContextAgent()
    assert agent.process_events([]) == "low"


def test_rrc_decision_agent() -> None:
    """Placeholder test for RRCDecisionAgent."""
    agent = RRCDecisionAgent()
    assert agent.generate_message({}, "low") == ""

