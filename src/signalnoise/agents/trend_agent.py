from signalnoise.agents.state import SignalNoiseState
from signalnoise.repository.signal_repository import SignalRepository
from signalnoise.repository.trend_repository import TrendRepository
from signalnoise.history.signal_history import SignalHistory
from signalnoise.history.trend_analyzer import TrendAnalyzer
from datetime import datetime
from signalnoise.observability.logger import logger

class TrendAgent:
    def __init__(self,trend_analyzer: TrendAnalyzer, signal_repo:SignalRepository, trend_repo:TrendRepository):
        self.trend_analyzer = trend_analyzer
        self.signal_repo = signal_repo
        self.trend_repo = trend_repo
    
    def _run_trend(self, state: SignalNoiseState):
        is_dict = isinstance(state, dict)
        analysis_mode = state.get("analysis_mode", None) if is_dict else getattr(state, "analysis_mode", None)

        if analysis_mode == "query":
            signal_history = state["signals"] if is_dict else state.signals
        else:
            signal_history = self.signal_repo.get_all()

        history = [
            SignalHistory(
                signal_type=signal.signal_type,
                severity=signal.severity,
                confidence=signal.confidence,
                detected_at=datetime.now()
            )
            for signal in signal_history
        ]

        trends = self.trend_analyzer.analyze_trends(history)

        for trend in trends:
            self.trend_repo.save(trend)

        logger.info(
            f"Generated {len(trends)} trends"
        )

        if is_dict:
            state["trends"] = trends
        else:
            state.trends = trends
            
        return state

    
    def __call__(self, state:SignalNoiseState):
        return self._run_trend(state)