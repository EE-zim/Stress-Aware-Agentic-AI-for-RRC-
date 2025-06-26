# Stress-Aware Agentic AI for RRC

This repository contains simple examples for a multi-agent system that controls 5G Radio Resource Control (RRC) messages with stress awareness. It includes:

- `stress_aware_controller_plan.md` – a design document describing log processing and stress-based prompting.
- `stress_aware_controller.py` – Python code to clean log data, compute stress levels, build prompts, and call the OpenAI API (e.g., GPT-4o).

Example usage:
```bash
python stress_aware_controller.py rrc_log.csv "UE requests handover" --api-key YOUR_OPENAI_KEY
```
This will print the detected stress level, show the generated prompt, and display the model's response.
