from signalnoise.agents.history_agent import (
    HistoryAgent
)

from signalnoise.agents.state import (
    SignalNoiseState
)

from signalnoise.repository.postgres_signal_repository import (
    PostgresSignalRepository
)

from signalnoise.signals.signal_model import (
    Signal
)


def test_history_agent():

    repo = (
        PostgresSignalRepository()
    )

    initial_count = (
        repo.count()
    )

    signal = Signal(
        signal_type="Dependency Risk",
        severity="High",
        confidence=0.95,
        evidence_chunks=[],
        summary="API dependency detected"
    )

    state = SignalNoiseState(
        query="dependency issue",
        signals=[signal]
    )

    agent = HistoryAgent(
        repo
    )

    agent(state)

    final_count = (
        repo.count()
    )

    print()
    print(
        f"Before: {initial_count}"
    )
    print(
        f"After: {final_count}"
    )

    assert final_count > initial_count