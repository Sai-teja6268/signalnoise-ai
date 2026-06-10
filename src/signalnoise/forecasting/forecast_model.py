from pydantic import BaseModel


class Forecast(BaseModel):
    signal_type: str

    current_risk: float

    predicted_risk_7_days: float

    predicted_risk_30_days: float

    recommendation: str