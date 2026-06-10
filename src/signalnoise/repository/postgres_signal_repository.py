from datetime import datetime

from signalnoise.database.connection import (
    SessionLocal
)

from signalnoise.database.models import (
    SignalRecord
)

from signalnoise.repository.signal_repository import (
    SignalRepository
)

from signalnoise.signals.signal_model import (
    Signal
)


class PostgresSignalRepository(
    SignalRepository
):

    def save(
        self,
        signal: Signal
    ):

        session = SessionLocal()

        try:

            record = SignalRecord(
                signal_type=signal.signal_type,
                severity=signal.severity,
                confidence=signal.confidence,
                summary=signal.summary,
                detected_at=datetime.now()
            )

            session.add(record)

            session.commit()

        finally:

            session.close()

    def get_all(
        self
    ) -> list[Signal]:

        session = SessionLocal()

        try:

            records = session.query(
                SignalRecord
            ).all()

            return [

                Signal(
                    signal_type=record.signal_type,
                    severity=record.severity,
                    confidence=record.confidence,
                    evidence_chunks=[],
                    summary=record.summary
                )

                for record in records
            ]

        finally:

            session.close()
    
    def count(self) -> int:

        session = SessionLocal()

        try:
            return (
                session.query(
                    SignalRecord
                ).count()
            )
        finally:
            session.close()

    def purge_for_testing(self):

        session = SessionLocal()

        try:
            session.query(
                SignalRecord
            ).delete()

            session.commit()

        finally:
            session.close()

    def get_by_signal_type(
    self,
        signal_type: str
    ) -> list[Signal]:

        session = SessionLocal()

        try:

            records = (
                session.query(
                    SignalRecord
                )
                .filter(
                    SignalRecord.signal_type == signal_type
                )
                .all()
            )

            return [

                Signal(
                    signal_type=r.signal_type,
                    severity=r.severity,
                    confidence=r.confidence,
                    evidence_chunks=[],
                    summary=r.summary
                )

                for r in records
            ]

        finally:
            session.close()