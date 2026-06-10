from signalnoise.agents.state import SignalNoiseState
from signalnoise.executive_summary.executive_summary_model import (
    ExecutiveSummary
)
from signalnoise.executive_summary.executive_summary_generator import (
    ExecutiveSummaryGenerator
)
from signalnoise.observability.logger import logger

class SummaryAgent:
    def __init__(self, summary_generator: ExecutiveSummaryGenerator):
        self.summary_generator = summary_generator

    def _run_summary(self, state: SignalNoiseState):
        """
        Generate Executive Summary
        """
        is_dict = isinstance(state, dict)
        analysis_mode = state.get("analysis_mode", None) if is_dict else getattr(state, "analysis_mode", None)

        if analysis_mode == "portfolio":
            from signalnoise.repository.postgres_risk_repository import PostgresRiskRepository
            from signalnoise.forecasting.forecast_engine import ForecastEngine
            
            risk_repo = PostgresRiskRepository()
            forecast_engine = ForecastEngine()
            
            risks = risk_repo.get_all()
            forecasts = [forecast_engine.forecast(r) for r in risks]
        else:
            risks = state.get("risks", []) if is_dict else getattr(state, "risks", [])
            forecasts = state.get("forecasts", []) if is_dict else getattr(state, "forecasts", [])

        if not risks:
            exec_summary = (
                ExecutiveSummary(
                    overall_risk="Low",
                    key_risks=[],
                    forecast_outlook="No forecast available",
                    summary="No risks detected"
                )
            )
            logger.info("Executive summary generated")
            if is_dict:
                state["executive_summary"] = exec_summary
            else:
                state.executive_summary = exec_summary
            return state
        
        max_risk = max(risks, key=lambda r: r.risk_score)

        key_risk=[
            f"{risk.signal_type} ({risk.severity})"
            for risk in risks
        ]

        forecast_outlook=""
        if forecasts:
            forecast_outlook= forecasts[0].recommendation
        
        exec_summary = (
            ExecutiveSummary(
                overall_risk=max_risk.severity,
                key_risks=key_risk,
                forecast_outlook=forecast_outlook,
                summary=(
                    f"Highest risk detected: "
                    f"{max_risk.signal_type}: {max_risk.explanation}. "
                    f"Forecast indicates: "
                    f"{forecast_outlook}"
                )
            )
        )

        logger.info("Executive summary generated")

        if is_dict:
            state["executive_summary"] = exec_summary
        else:
            state.executive_summary = exec_summary

        return state


    def __call__(self, state: SignalNoiseState):
        return self._run_summary(state)