from pydantic import BaseModel
from typing import List


class ExecutiveSummary(BaseModel):

    overall_risk: str

    key_risks: List[str]

    forecast_outlook: str

    summary: str