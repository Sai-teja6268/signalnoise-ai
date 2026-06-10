from pydantic import BaseModel
from typing import List

class Signal(
    BaseModel
):
    signal_type: str
    severity: str
    confidence: float
    evidence_chunks: List[str]
    summary: str
