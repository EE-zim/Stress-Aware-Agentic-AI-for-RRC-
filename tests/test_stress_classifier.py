"""Tests for stress_classifier module."""
from stress_classifier import stress_rules


def test_classify_low():
    level = stress_rules.classify({})
    assert level == "Low"
