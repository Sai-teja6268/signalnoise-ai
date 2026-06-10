from signalnoise.repository.postgres_trend_repository import (
    PostgresTrendRepository
)

from signalnoise.trends.trend_model import (
    Trend
)


def test_trend_repository():

    repo = (
        PostgresTrendRepository()
    )

    trend = Trend(
        signal_type="Dependency Risk",
        trend_detection="Increasing",
        growth_rate=3.0,
        explaination="3 signals detected"
    )

    repo.save(trend)

    trends = repo.get_all()

    print()

    for item in trends:
        print(item)

    assert len(trends) > 0