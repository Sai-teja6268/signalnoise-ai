from signalnoise.forecasting.forecast_engine import (
    ForecastEngine
)

from signalnoise.forecasting.forecast_agent import (
    ForecastAgent
)

from signalnoise.risk.risk_model import (
    Risk
)

from signalnoise.agents.state import (
    SignalNoiseState
)


def test_forecast_agent():

    risk = Risk(
        signal_type="Dependency Risk",
        risk_score=85.5,
        severity="High",
        explanation=""
    )

    state = SignalNoiseState(
        query="dependency issue",
        risks=[risk]
    )

    agent = ForecastAgent(
        ForecastEngine()
    )

    updated_state = agent(
        state
    )

    print()
    print(
        updated_state.forecasts
    )

    assert len(
        updated_state.forecasts
    ) == 1