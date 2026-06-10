from fastapi import APIRouter, HTTPException
from typing import List
from signalnoise.risk.risk_model import Risk
from signalnoise.repository.postgres_risk_repository import PostgresRiskRepository
from signalnoise.observability.logger import logger

router = APIRouter(
    prefix="/risks",
    tags=["risks"]
)

@router.get("", response_model=List[Risk])
def get_all_risks():
    logger.info("API request to fetch all risks")
    try:
        repo = PostgresRiskRepository()
        return repo.get_all()
    except Exception as e:
        logger.error(f"Failed to fetch risks: {e}")
        raise HTTPException(status_code=500, detail=str(e))
