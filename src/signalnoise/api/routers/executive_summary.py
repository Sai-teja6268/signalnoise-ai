from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from signalnoise.repository.postgres_risk_repository import PostgresRiskRepository
from signalnoise.forecasting.forecast_engine import ForecastEngine
from signalnoise.observability.logger import logger

router = APIRouter(
    prefix="/executive-summary",
    tags=["executive-summary"]
)

class ExecutiveSummaryResponse(BaseModel):
    overall_risk: str
    top_risks: List[str]
    forecast: str
    summary: str

@router.get("", response_model=ExecutiveSummaryResponse)
def get_executive_summary():
    try:
        risk_repo = PostgresRiskRepository()
        forecast_engine = ForecastEngine()
        
        risks = risk_repo.get_all()
        forecasts = [forecast_engine.forecast(r) for r in risks]
        
        if not risks:
            return ExecutiveSummaryResponse(
                overall_risk="Low",
                top_risks=[],
                forecast="No forecast available",
                summary="No risks detected"
            )
        
        max_risk = max(risks, key=lambda r: r.risk_score)
        top_risks = [f"{risk.signal_type} ({risk.severity})" for risk in risks]
        forecast = forecasts[0].recommendation if forecasts else "No forecast available"
        summary = f"Highest risk detected: {max_risk.signal_type}: {max_risk.explanation}. Forecast indicates: {forecast}"
        
        return ExecutiveSummaryResponse(
            overall_risk=max_risk.severity,
            top_risks=top_risks,
            forecast=forecast,
            summary=summary
        )
    except Exception as e:
        logger.error(f"Failed to generate executive summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))
