from datetime import datetime

from signalnoise.database.connection import (
    SessionLocal
)

from signalnoise.database.models import (
    TrendRecord
)

from signalnoise.repository.trend_repository import (
    TrendRepository
)

from signalnoise.trends.trend_model import (
    Trend
)


class PostgresTrendRepository(
    TrendRepository
):

    def save(
        self,
        trend: Trend
    ):

        session = SessionLocal()

        try:

            record = TrendRecord(
                signal_type=trend.signal_type,
                trend_detection=trend.trend_detection,
                growth_rate=trend.growth_rate,
                created_at=datetime.now()
            )

            session.add(record)

            session.commit()

        finally:

            session.close()

    def get_all(
        self
    ) -> list[Trend]:

        session = SessionLocal()

        try:

            records = session.query(
                TrendRecord
            ).all()

            return [

                Trend(
                    signal_type=record.signal_type,
                    trend_detection=record.trend_detection,
                    growth_rate=record.growth_rate,
                    explaination=f"{record.growth_rate} signals detected"
                )

                for record in records
            ]

        finally:

            session.close()