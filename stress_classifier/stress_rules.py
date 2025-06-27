"""Rule-based stress classification."""

from typing import Dict


THRESHOLDS = {
    "high": 10,
    "medium": 3,
}


def classify(features: Dict[str, float]) -> str:
    """Return stress level based on features."""
    # TODO: Replace with real rules
    if features.get("critical_count", 0) > 5 or features.get("events_per_sec", 0) > THRESHOLDS["high"]:
        return "High"
    if features.get("critical_count", 0) > 0 or features.get("events_per_sec", 0) > THRESHOLDS["medium"]:
        return "Medium"
    return "Low"
