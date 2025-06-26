import pandas as pd
import json
from dataclasses import dataclass
from typing import List, Dict, Any
import openai

@dataclass
class Event:
    time: str
    message: str
    protocol: str
    source: str
    dest: str


def clean_rrc_log(file_path: str) -> List[Event]:
    """Read a semicolon-separated log CSV and remove rows with missing
    mandatory columns."""
    df = pd.read_csv(file_path, sep=';')
    df = df.dropna(subset=['Time', 'Message name', 'Protocol'])
    events = [
        Event(
            time=row['Time'],
            message=row['Message name'],
            protocol=row['Protocol'],
            source=row.get('From', ''),
            dest=row.get('To', '')
        )
        for _, row in df.iterrows()
    ]
    return events


def compute_features(events: List[Event]) -> Dict[str, Any]:
    """Compute simple features from events."""
    if not events:
        return {"total_events": 0, "events_per_sec": 0, "critical_count": 0}

    times = pd.to_datetime([e.time for e in events])
    duration = (times[-1] - times[0]).total_seconds() or 1
    total = len(events)
    events_per_sec = total / duration
    critical_msgs = [e for e in events if e.message in ["HandoverRequired", "rrcRelease", "RLF_indication"]]
    return {
        "total_events": total,
        "events_per_sec": events_per_sec,
        "critical_count": len(critical_msgs),
        "duration_sec": duration,
    }


def label_stress_level(features: Dict[str, Any]) -> str:
    """Assign stress level based on simple thresholds."""
    if features["critical_count"] > 5 or features["events_per_sec"] > 10:
        return "High"
    if features["critical_count"] > 0 or features["events_per_sec"] > 3:
        return "Medium"
    return "Low"


def build_scenario_json(events: List[Event], features: Dict[str, Any]) -> str:
    stress = label_stress_level(features)
    payload = {
        "metadata": {
            "stress_level": stress,
            **features
        },
        "events": [e.__dict__ for e in events]
    }
    return json.dumps(payload, indent=2)


TEMPLATES = {
    "Low": (
        "System: You are a 5G RRC control agent.\n"
        "Context: Network stable.\n"
        "Situation: {description}\n"
        "Instruction: Provide the correct RRC message and explain calmly."
    ),
    "Medium": (
        "System: You are a 5G RRC control agent.\n"
        "Context: Network load increasing.\n"
        "Situation: {description}\n"
        "Instruction: Respond promptly with the correct RRC message and a short explanation."
    ),
    "High": (
        "System: You are a 5G RRC control agent. Critical condition!\n"
        "Context: Heavy stress – immediate action required.\n"
        "Situation: {description}\n"
        "Instruction: Respond immediately with the RRC message and a short explanation."
    ),
}


def make_prompt(description: str, stress: str) -> str:
    template = TEMPLATES.get(stress, TEMPLATES["Low"])
    return template.format(description=description)


def send_to_gpt4o(prompt: str, *, api_key: str, model: str = "gpt-4o") -> str:
    """Call the OpenAI API using the given prompt."""
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"].strip()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Stress-aware RRC agent")
    parser.add_argument("log", help="Path to RRC log file")
    parser.add_argument("description", help="Short description of current event")
    parser.add_argument("--api-key", required=True, help="OpenAI API key")
    args = parser.parse_args()

    events = clean_rrc_log(args.log)
    features = compute_features(events)
    stress = label_stress_level(features)
    prompt = make_prompt(args.description, stress)
    print("Stress level:", stress)
    print("Prompt:\n", prompt)
    reply = send_to_gpt4o(prompt, api_key=args.api_key)
    print("\nLLM Response:\n", reply)
