from datetime import datetime

from signalnoise.database.connection import (
    SessionLocal
)

from signalnoise.database.models import (
    RiskRecord
)

from signalnoise.repository.risk_repository import (
    RiskRepository
)

from signalnoise.risk.risk_model import (
    Risk
)


class PostgresRiskRepository(
    RiskRepository
):

    def save(
        self,
        risk: Risk
    ):

        session = SessionLocal()

        try:

            record = RiskRecord(
                signal_type=risk.signal_type,
                risk_score=risk.risk_score,
                severity=risk.severity,
                explanation=risk.explanation,
                created_at=datetime.now()
            )

            session.add(record)

            session.commit()

        finally:

            session.close()

    def get_all(
        self
    ) -> list[Risk]:

        session = SessionLocal()

        try:

            records = (
                session.query(
                    RiskRecord
                ).all()
            )

            return [

                Risk(
                    signal_type=record.signal_type,
                    risk_score=record.risk_score,
                    severity=record.severity,
                    explanation=record.explanation
                )

                for record in records
            ]

        finally:

            session.close()

    def count(
        self
    ) -> int:

        session = SessionLocal()

        try:

            return (
                session.query(
                    RiskRecord
                ).count()
            )

        finally:

            session.close()

    def purge_for_testing(
        self
    ):

        session = SessionLocal()

        try:

            session.query(
                RiskRecord
            ).delete()

            session.commit()

        finally:

            session.close()