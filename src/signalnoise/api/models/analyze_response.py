from pydantic import BaseModel
from typing import List, Optional
from signalnoise.retrieval.retrieval_result import RetrievalResult
from signalnoise.signals.signal_model import Signal
from signalnoise.trends.trend_model import Trend
from signalnoise.risk.risk_model import Risk
from signalnoise.forecasting.forecast_model import Forecast
from signalnoise.executive_summary.executive_summary_model import ExecutiveSummary

class AnalyzeResponse(BaseModel):
    query: str
    retrieval_results: List[RetrievalResult]
    signals: List[Signal]
    trends: List[Trend]
    risks: List[Risk]
    forecasts: List[Forecast]
    executive_summary: Optional[ExecutiveSummary] = None
    historical_analysis: bool = True
