from fastapi import APIRouter, HTTPException
from typing import List
from signalnoise.signals.signal_model import Signal
from signalnoise.repository.postgres_signal_repository import PostgresSignalRepository
from signalnoise.observability.logger import logger

router = APIRouter(
    prefix="/signals",
    tags=["signals"]
)

@router.get("", response_model=List[Signal])
def get_all_signals():
    logger.info("API request to fetch all signals")
    try:
        repo = PostgresSignalRepository()
        return repo.get_all()
    except Exception as e:
        logger.error(f"Failed to fetch signals: {e}")
        raise HTTPException(status_code=500, detail=str(e))
