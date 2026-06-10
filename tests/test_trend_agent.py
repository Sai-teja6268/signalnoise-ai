from signalnoise.agents.trend_agent import TrendAgent
from signalnoise.history.trend_analyzer import TrendAnalyzer
from signalnoise.signals.signal_model import Signal
from signalnoise.repository.postgres_signal_repository import PostgresSignalRepository
from signalnoise.repository.postgres_trend_repository import PostgresTrendRepository

def test_trend_agent():
    state = {
        "query": "delivery blockers",
        "retrieval_results": [],
        "signals": [
            Signal(
                signal_type="Dependency Risk",
                severity="High",
                confidence=0.9,
                evidence_chunks=["1_chunk_0"],
                summary="Dependency issue"
            ),
            Signal(
                signal_type="Dependency Risk",
                severity="High",
                confidence=0.9,
                evidence_chunks=["1_chunk_1"],
                summary="Dependency issue"
            ),
            Signal(
                signal_type="Dependency Risk",
                severity="High",
                confidence=0.9,
                evidence_chunks=["1_chunk_2"],
                summary="Dependency issue"
            )
        ],
        "trends": [],
        "risks": [],
        "executive_summary": None
    }

    signal_repo = PostgresSignalRepository()
    trend_repo = PostgresTrendRepository()

    agent = TrendAgent(
        signal_repo=signal_repo,
        trend_repo=trend_repo,
        trend_analyzer=TrendAnalyzer()
    )


    updated_state = agent(state)

    print()
    print(updated_state["trends"])

    assert len(updated_state["trends"]) > 0