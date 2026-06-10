from signalnoise.repository.postgres_signal_repository import (
    PostgresSignalRepository
)

from signalnoise.signals.signal_model import (
    Signal
)


def test_signal_repository():

    repo = (
        PostgresSignalRepository()
    )

    signal = Signal(
        signal_type="Dependency Risk",
        severity="High",
        confidence=0.9,
        evidence_chunks=[],
        summary="API dependency detected"
    )

    repo.save(signal)

    signals = repo.get_all()

    print()

    for item in signals:

        print(item)

    assert len(signals) > 0