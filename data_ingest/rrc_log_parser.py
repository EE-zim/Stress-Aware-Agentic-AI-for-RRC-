"""Data ingestion utilities for RRC logs."""

from typing import List, Dict
import csv
import json


def parse_csv_to_events(csv_path: str) -> List[Dict[str, str]]:
    """Parse a semicolon-separated RRC log CSV into a list of events."""
    # TODO: Implement parsing logic
    events: List[Dict[str, str]] = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            events.append(dict(row))
    return events


def events_to_json(events: List[Dict[str, str]]) -> str:
    """Convert events to a JSON string."""
    # TODO: Add additional processing if needed
    return json.dumps(events, indent=2)

