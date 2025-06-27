# Stress-Aware Agentic AI for RRC

This project provides a scaffold for a stress-aware multi-agent controller for 5G Radio Resource Control (RRC).
It includes placeholders for data ingestion, stress classification, agent logic, and a FastAPI service.

## Structure
- `data_ingest/` – utilities to parse RRC log CSV files
- `stress_classifier/` – rule-based stress level labeler
- `agents/` – network context and decision agents
- `api/` – FastAPI application exposing trigger and status endpoints
- `tests/` – pytest suite

## Development
Install dependencies and run tests:
```bash
python -m pip install -r requirements.txt
pytest
```

Run the API locally:
```bash
uvicorn api.main:app --reload
```

A `Dockerfile` is provided for containerized deployment.
