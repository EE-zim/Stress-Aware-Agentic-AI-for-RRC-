"""Tests for agent scaffolding."""
from agents import network_context, rrc_decision


def test_network_context_stub():
    agent = network_context.NetworkContextAgent()
    try:
        agent.process_events([])
    except NotImplementedError:
        pass
    else:
        assert False, "Expected NotImplementedError"


def test_rrc_decision_stub():
    agent = rrc_decision.RRCDecisionAgent(None)
    try:
        agent.generate("prompt")
    except NotImplementedError:
        pass
    else:
        assert False, "Expected NotImplementedError"
