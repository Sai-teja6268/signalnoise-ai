from pydantic import BaseModel

class Trend(BaseModel):
    signal_type: str
    trend_detection: str
    growth_rate: float
    explaination: str