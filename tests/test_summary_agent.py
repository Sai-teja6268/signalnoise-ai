from signalnoise.agents.summary_agent import (
    SummaryAgent
)
from signalnoise.executive_summary.executive_summary_generator import (
    ExecutiveSummaryGenerator
)
from signalnoise.risk.risk_model import (
    Risk
)
from signalnoise.forecasting.forecast_model import (
    Forecast
)

def test_summary_agent_with_risks_and_forecasts():
    state = {
        "query": "delivery blockers",
        "retrieval_results": [],
        "signals": [],
        "trends": [],
        "risks": [
            Risk(
                signal_type="Dependency Risk",
                risk_score=90,
                severity="High",
                explanation="Dependency delays detected"
            ),
            Risk(
                signal_type="Testing Risk",
                risk_score=60,
                severity="Medium",
                explanation="Testing delays detected"
            )
        ],
        "forecasts": [
            Forecast(
                signal_type="Dependency Risk",
                current_risk=85.5,
                predicted_risk_7_days=89.78,
                predicted_risk_30_days=98.32,
                recommendation="Immediate leadership intervention required"
            )
        ],
        "executive_summary": None
    }

    agent = SummaryAgent(
        ExecutiveSummaryGenerator()
    )

    updated_state = agent(state)
    summary = updated_state["executive_summary"]

    print(summary)

    assert summary is not None
    assert summary.overall_risk == "High"
    assert summary.key_risks == ["Dependency Risk (High)", "Testing Risk (Medium)"]
    assert summary.forecast_outlook == "Immediate leadership intervention required"
    assert "Highest risk detected" in summary.summary
    assert "Dependency Risk: Dependency delays detected" in summary.summary
    assert "Forecast indicates: Immediate leadership intervention required" in summary.summary



def test_summary_agent_with_no_risks():
    state = {
        "query": "delivery blockers",
        "retrieval_results": [],
        "signals": [],
        "trends": [],
        "risks": [],
        "executive_summary": None
    }

    agent = SummaryAgent(
        ExecutiveSummaryGenerator()
    )

    updated_state = agent(state)
    summary = updated_state["executive_summary"]

    print(summary)

    assert summary is not None
    assert summary.overall_risk == "Low"
    assert summary.key_risks == []
    assert summary.forecast_outlook == "No forecast available"
    assert summary.summary == "No risks detected"
