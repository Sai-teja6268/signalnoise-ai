from fastapi import APIRouter, HTTPException
from typing import List
from signalnoise.forecasting.forecast_model import Forecast
from signalnoise.repository.postgres_risk_repository import PostgresRiskRepository
from signalnoise.forecasting.forecast_engine import ForecastEngine
from signalnoise.observability.logger import logger

router = APIRouter(
    prefix="/forecasts",
    tags=["forecasts"]
)

@router.get("", response_model=List[Forecast])
def get_all_forecasts():
    logger.info("API request to generate forecasts from saved risks")
    try:
        risk_repo = PostgresRiskRepository()
        risks = risk_repo.get_all()
        
        forecast_engine = ForecastEngine()
        forecasts = []
        for risk in risks:
            forecasts.append(forecast_engine.forecast(risk))
        return forecasts
    except Exception as e:
        logger.error(f"Failed to generate forecasts: {e}")
        raise HTTPException(status_code=500, detail=str(e))
