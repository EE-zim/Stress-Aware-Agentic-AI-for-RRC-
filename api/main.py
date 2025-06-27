"""FastAPI application for RRC controller."""

from fastapi import FastAPI

app = FastAPI(title="Stress-Aware RRC Controller")


@app.post("/trigger")
async def trigger_controller() -> dict:
    """Trigger processing of latest events."""
    # TODO: Implement trigger logic
    return {"status": "pending"}


@app.get("/status")
async def get_status() -> dict:
    """Get current controller status."""
    # TODO: Return real status
    return {"status": "idle"}
