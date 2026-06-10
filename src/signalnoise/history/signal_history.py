from datetime import datetime
from pydantic import BaseModel


class SignalHistory(BaseModel):

    signal_type: str

    confidence: float

    severity: str

    detected_at: datetime