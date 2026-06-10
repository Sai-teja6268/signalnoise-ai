from signalnoise.risk.risk_model import (
    Risk
)

from signalnoise.executive_summary.executive_summary_generator import (
    ExecutiveSummaryGenerator
)


def test_executive_summary():

    risks = [

        Risk(
            signal_type="DependencyRisk",
            risk_score=90,
            severity="High",
            explanation="Dependency delays detected"
        ),

        Risk(
            signal_type="TestingRisk",
            risk_score=60,
            severity="Medium",
            explanation="Testing delays detected"
        )
    ]

    generator = (
        ExecutiveSummaryGenerator()
    )

    summary = generator.generate_summary(
        risks
    )

    print("\n\n")

    print(summary)

    assert summary.overall_risk == "High"