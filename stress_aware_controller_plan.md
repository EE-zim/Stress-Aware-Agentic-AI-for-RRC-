# Stress-Aware Multi-Agent LLM RRC Controller – Implementation Plan

This document describes a Python-based approach for building a stress-aware multi-agent controller for 5G Radio Resource Control (RRC). The plan includes log preprocessing, stress assessment, real-time prompt generation, and prompt templates for the LLM agents.

## 1. RRC Log Processing and Stress Labeling

1. **Parse Logs**: Load RRC logs (e.g., CSV files) with `pandas`.
2. **Feature Extraction**: Calculate message rates, timing gaps, counts of critical events, etc.
3. **Rule-Based Stress Levels**:
   - **Low**: Routine activity, low event rate.
   - **Medium**: Noticeable activity or occasional critical messages.
   - **High**: Burst of events or repeated failures.
4. **Scenario JSON**: For each period, create a JSON structure with metadata, events, and derived features including the stress label.

```python
import pandas as pd

# parse logs
log = pd.read_csv('rrc_log.csv', sep=';')

events = [
    {
        'time': row['Time'],
        'message': row['Message name'],
        'protocol': row['Protocol'],
    }
    for _, row in log.iterrows()
]

# compute features
rate = len(events) / max((pd.to_datetime(events[-1]['time']) - pd.to_datetime(events[0]['time'])).total_seconds(), 1)
critical = sum(e['message'] in ['HandoverRequired', 'rrcRelease'] for e in events)

# label stress
if critical > 5 or rate > 10:
    stress = 'High'
elif critical > 0 or rate > 3:
    stress = 'Medium'
else:
    stress = 'Low'

scenario = {
    'metadata': {'stress_level': stress},
    'events': events,
}
```

## 2. Prompt Generation Based on Stress

Construct the LLM prompt with a brief stress cue:

```python
def make_prompt(event_desc, stress):
    system = (
        'You are an RRC controller. Output the correct 3GPP-compliant RRC message '
        'and a short explanation.'
    )
    if stress == 'High':
        urgency = 'Urgency: High - Critical situation, respond immediately.'
    elif stress == 'Medium':
        urgency = 'Urgency: Medium - Elevated load, respond promptly.'
    else:
        urgency = 'Urgency: Low - Network stable.'
    return f"{system}\n{urgency}\nSituation: {event_desc}\nResponse:"""
```

## 3. Multi-Agent Loop

- **Network Context Agent**: Monitors logs or events, computes stress, and builds the prompt.
- **RRC Decision Agent**: LLM that generates the RRC message and explanation using the prompt.

```python
class ContextAgent:
    def __init__(self, llm):
        self.llm = llm

    def handle(self, event_desc, events):
        # compute stress
        features = compute_features(events)
        stress = label_stress_level(features)
        prompt = make_prompt(event_desc, stress)
        return self.llm.generate(prompt)
```

## 4. Stress Level Prompt Templates

Low:
```
System: You are a 5G RRC agent.
Context: Network stable.
Situation: <description>
Instruction: Provide the appropriate RRC message and explain calmly.
```

Medium:
```
System: You are a 5G RRC agent.
Context: Network load increasing.
Situation: <description>
Instruction: Respond promptly with the correct RRC message and a brief explanation.
```

High:
```
System: You are a 5G RRC agent. Critical condition!
Context: Heavy stress – immediate action required.
Situation: <description>
Instruction: Respond immediately with the RRC message and a short explanation.
```

A relaxation prompt can be injected after prolonged high stress:
```
System: (Internal) Take a brief pause and ensure clarity before continuing.
```

## 5. Testing and Validation

- Verify that generated RRC messages match expected messages.
- Measure explanation quality and latency.
- Log outcomes per stress level to analyze performance.

This plan describes the main components for implementing a stress-aware multi-agent RRC controller leveraging LLM prompting.
