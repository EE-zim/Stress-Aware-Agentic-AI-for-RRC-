"""FastAPI application exposing controller endpoints."""

from fastapi import FastAPI

app = FastAPI(title="Stress-Aware RRC Controller")


@app.post("/trigger")
async def trigger_event() -> dict:
    """Trigger processing of a new event.

    TODO: Accept event data and invoke agents.
    """
    return {"status": "not_implemented"}


@app.get("/status")
async def status() -> dict:
    """Return current system status."""
    # TODO: Provide real status information
    return {"status": "ok"}

