from signalnoise.retrieval.retrieval_result import (
    RetrievalResult
)

from signalnoise.signals.signal_model import (
    Signal
)

from signalnoise.trends.trend_model import (
    Trend
)

from signalnoise.risk.risk_model import (
    Risk
)

from signalnoise.executive_summary.executive_summary_model import (
    ExecutiveSummary
)

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from signalnoise.forecasting.forecast_model import (
    Forecast
)

class SignalNoiseState(BaseModel):
    query: str
    retrieval_results: List[RetrievalResult] = Field(default_factory=list)
    signals: List[Signal] = Field(default_factory=list)
    trends: List[Trend] = Field(default_factory=list)
    risks: List[Risk] = Field(default_factory=list)
    executive_summary: Optional[ExecutiveSummary] = None
    forecasts: List[Forecast] = Field(default_factory=list)
    historical_analysis: bool = True
    analysis_mode: str = "query"
    document_type: Optional[str] = None
    source: Optional[str] = None

    @field_validator("document_type", "source", mode="before")
    @classmethod
    def clean_placeholder_strings(cls, v):
        if isinstance(v, str) and v.lower().strip() in ("string", "none", ""):
            return None
        return v

    