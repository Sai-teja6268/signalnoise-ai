from fastapi import FastAPI
from .api.health import router as health_router

app = FastAPI(
    title="SignalNoise AI",
    description="Enterprise AI platform that surfaces weak signals hidden in organizational communications.",
    version="1.0.0"
)

app.include_router(health_router)

@app.get("/")
def read_root():
    return {"message": "SignalNoiseAI is running"}
