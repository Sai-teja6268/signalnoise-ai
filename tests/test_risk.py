from signalnoise.risk.risk_engine import (
    RiskEngine
)

from signalnoise.trends.trend_model import (
    Trend
)


def test_risk_engine_v2():

    trend = Trend(
        signal_type="Dependency Risk",
        trend_detection="Increasing",
        growth_rate=200,
        explaination=""
    )

    engine = RiskEngine()

    risk = engine.calculate_risk(
        trend=trend,
        confidence=0.95,
        severity="High",
        signal_count=10
    )

    print(risk)

    assert risk.risk_score > 80