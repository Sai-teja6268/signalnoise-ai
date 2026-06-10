from unittest.mock import MagicMock

from signalnoise.agents.risk_agent import (
    RiskAgent
)

from signalnoise.trends.trend_model import (
    Trend
)

from signalnoise.signals.signal_model import (
    Signal
)

from signalnoise.risk.risk_engine import (
    RiskEngine
)


def test_risk_agent():

    state = {
        "trends": [
            Trend(
                signal_type="Dependency Risk",
                trend_detection="Increasing",
                growth_rate=200.0,
                explaination=""
            )
        ]
    }

    signal_repo = MagicMock()

    signal_repo.get_by_signal_type.return_value = [

        Signal(
            signal_type="Dependency Risk",
            severity="High",
            confidence=0.95,
            evidence_chunks=[],
            summary="Dependency issue"
        )

    ]

    risk_repo = MagicMock()

    agent = RiskAgent(
        risk_engine=RiskEngine(),
        signal_repo=signal_repo,
        risk_repo=risk_repo
    )

    updated_state = agent(state)

    print()
    print(updated_state["risks"])

    assert len(updated_state["risks"]) > 0

    assert (
        risk_repo.save.call_count == 1
    )