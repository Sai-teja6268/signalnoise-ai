from signalnoise.services.signalnoise_service import (
    SignalNoiseService
)

from unittest.mock import MagicMock
from signalnoise.agents.agents_factory import AgentsFactory
from signalnoise.workflow.graph import SignalNoiseGraph
from signalnoise.services.ingestion_service import IngestionService
from signalnoise.ingestion.processor import DocumentProcessor
from signalnoise.rag.chunking_service import ChunkingService
from signalnoise.database.connection import SessionLocal
from signalnoise.database.models import SignalRecord, TrendRecord, RiskRecord
from signalnoise.repository.postgres_signal_repository import PostgresSignalRepository
from signalnoise.signals.signal_model import Signal

def test_service():

    mock_graph = MagicMock()

    mock_graph.invoke.return_value = {
        "executive_summary": "success"
    }

    service = SignalNoiseService(
        mock_graph
    )

    result = service.analyze(
        "delivery blockers"
    )

    print()
    print(result)

    assert result is not None


def test_service_integration():
    # 0. Clean database and seed exactly 1 signal so overall risk is Low
    session = SessionLocal()
    try:
        session.query(SignalRecord).delete()
        session.query(TrendRecord).delete()
        session.query(RiskRecord).delete()
        session.commit()
    finally:
        session.close()

    signal_repo = PostgresSignalRepository()
    signal_repo.save(
        Signal(
            signal_type="Dependency Risk",
            severity="Low",
            confidence=0.9,
            evidence_chunks=["1_chunk_0"],
            summary="Dependency issue"
        )
    )

    # 1. Ingest and chunk documents
    ingestion = IngestionService()
    processor = DocumentProcessor()
    chunker = ChunkingService()

    docs = ingestion.ingest("data/sample/meeting_notes.txt")
    lc_docs = processor.process_documents(docs)
    chunks = chunker.chunk_documents(lc_docs)

    # 2. Create agents using factory
    retrieval_agent = AgentsFactory.create_retrieval_agent(chunks)
    signal_agent = AgentsFactory.create_signal_agent()
    history_agent = AgentsFactory.create_history_agent()
    trend_agent = AgentsFactory.create_trend_agent()
    risk_agent = AgentsFactory.create_risk_agent()
    forecast_agent = AgentsFactory.create_forecast_agent()
    summary_agent = AgentsFactory.create_summary_agent()

    # 3. Initialize graph
    graph = SignalNoiseGraph(
        retrieval_agent=retrieval_agent,
        signal_agent=signal_agent,
        history_agent=history_agent,
        trend_agent=trend_agent,
        risk_agent=risk_agent,
        forecast_agent=forecast_agent,
        summary_agent=summary_agent
    )

    # 4. Initialize service with real graph
    service = SignalNoiseService(graph)

    # 5. Analyze and assert
    result = service.analyze("delivery blockers")

    assert result is not None
    assert len(result["retrieval_results"]) > 0
    assert len(result["signals"]) > 0
    assert len(result["trends"]) > 0
    assert len(result["risks"]) > 0
    assert len(result["forecasts"]) > 0
    assert result["executive_summary"] is not None
    assert result["executive_summary"].overall_risk == "Medium"