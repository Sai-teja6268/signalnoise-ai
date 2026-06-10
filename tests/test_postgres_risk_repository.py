from signalnoise.repository.postgres_risk_repository import (
    PostgresRiskRepository
)

from signalnoise.risk.risk_model import (
    Risk
)


def test_risk_repository():

    repo = (
        PostgresRiskRepository()
    )

    risk = Risk(
        signal_type="Dependency Risk",
        risk_score=90.0,
        severity="High",
        explanation="Trend Growth Rate: 3.0"
    )

    repo.save(
        risk
    )

    risks = repo.get_all()

    print()

    for item in risks:

        print(item)

    assert len(risks) > 0