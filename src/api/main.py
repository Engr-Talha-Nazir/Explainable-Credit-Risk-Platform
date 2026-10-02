from fastapi import FastAPI

app = FastAPI(
    title="Explainable Credit Risk API",
    description="API for explainable and fair credit risk predictions",
    version="0.1.0",
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "version": "0.1.0"}
