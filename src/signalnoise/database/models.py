from datetime import datetime

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)


class Base(DeclarativeBase):
    pass


class SignalRecord(Base):

    __tablename__ = "signals"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    signal_type: Mapped[str]

    severity: Mapped[str]

    confidence: Mapped[float]

    summary: Mapped[str]

    detected_at: Mapped[datetime]


class TrendRecord(Base):

    __tablename__ = "trends"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    signal_type: Mapped[str]

    trend_detection: Mapped[str]

    growth_rate: Mapped[float]

    created_at: Mapped[datetime]


class RiskRecord(Base):

    __tablename__ = "risks"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    signal_type: Mapped[str]

    risk_score: Mapped[float]

    severity: Mapped[str]

    explanation: Mapped[str]

    created_at: Mapped[datetime]
