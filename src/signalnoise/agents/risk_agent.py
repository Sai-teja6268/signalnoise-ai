from signalnoise.agents.state import SignalNoiseState
from signalnoise.risk.risk_engine import RiskEngine
from signalnoise.risk.risk_model import Risk
from signalnoise.repository.risk_repository import RiskRepository
from signalnoise.repository.signal_repository import SignalRepository
from signalnoise.observability.logger import logger

class RiskAgent:
    def __init__(self,risk_engine:RiskEngine,risk_repo:RiskRepository,  signal_repo:SignalRepository):
        self.risk_engine = risk_engine
        self.risk_repo = risk_repo
        self.signal_repo = signal_repo
    
    def _run_risk(self, state: SignalNoiseState):
        is_dict = isinstance(state, dict)
        trends = state["trends"] if is_dict else state.trends
        analysis_mode = state.get("analysis_mode", None) if is_dict else getattr(state, "analysis_mode", None)

        risks = []
        for trend in trends:
            if analysis_mode == "query":
                state_signals = state["signals"] if is_dict else state.signals
                signals = [s for s in state_signals if s.signal_type == trend.signal_type]
            else:
                signals = self.signal_repo.get_by_signal_type(trend.signal_type)

            if not signals:
                continue
            latest_signal = signals[-1]

            risk = self.risk_engine.calculate_risk(
                trend=trend,
                confidence=latest_signal.confidence,
                severity=latest_signal.severity,
                signal_count=len(signals)
            )
            
            self.risk_repo.save(risk)
            risks.append(risk)
        
        logger.info(
            f"Calculated {len(risks)} risks"
        )

        if is_dict:
            state["risks"] = risks
        else:
            state.risks = risks
        return state

    def __call__(self, state:SignalNoiseState):
        return self._run_risk(state)