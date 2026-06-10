from fastapi import FastAPI
from signalnoise.api.routers.analyze import router as analyze_router
from signalnoise.api.routers.signals import router as signals_router
from signalnoise.api.routers.trends import router as trends_router
from signalnoise.api.routers.risks import router as risks_router
from signalnoise.api.routers.forecasts import router as forecasts_router
from signalnoise.api.documents import router as documents_router
from signalnoise.api.routers.health import router as health_router
from signalnoise.api.routers.version import router as version_router
from signalnoise.api.routers.executive_summary import router as executive_summary_router

app = FastAPI(
    title="SignalNoise AI",
    description="Enterprise AI platform that surfaces weak signals hidden in organizational communications.",
    version="1.0.0"
)

app.include_router(health_router)
app.include_router(version_router)
app.include_router(documents_router)
app.include_router(analyze_router)
app.include_router(signals_router)
app.include_router(trends_router)
app.include_router(risks_router)
app.include_router(forecasts_router)
app.include_router(executive_summary_router)

@app.get("/")
def read_root():
    return {"message": "SignalNoiseAI is running"}
