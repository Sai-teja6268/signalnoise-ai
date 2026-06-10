from fastapi import APIRouter, HTTPException
from typing import List
from signalnoise.trends.trend_model import Trend
from signalnoise.repository.postgres_trend_repository import PostgresTrendRepository
from signalnoise.observability.logger import logger

router = APIRouter(
    prefix="/trends",
    tags=["trends"]
)

@router.get("", response_model=List[Trend])
def get_all_trends():
    logger.info("API request to fetch all trends")
    try:
        repo = PostgresTrendRepository()
        return repo.get_all()
    except Exception as e:
        logger.error(f"Failed to fetch trends: {e}")
        raise HTTPException(status_code=500, detail=str(e))
