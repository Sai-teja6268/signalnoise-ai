from pydantic import BaseModel

class Risk(BaseModel):

    signal_type: str

    risk_score: float

    severity: str

    explanation: str