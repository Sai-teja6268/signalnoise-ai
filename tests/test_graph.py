from signalnoise.agents.agents_factory import AgentsFactory
from signalnoise.workflow.graph import SignalNoiseGraph
from signalnoise.services.ingestion_service import IngestionService
from signalnoise.ingestion.processor import DocumentProcessor
from signalnoise.rag.chunking_service import ChunkingService
from signalnoise.agents.state import SignalNoiseState
from signalnoise.database.connection import SessionLocal
from signalnoise.database.models import SignalRecord, TrendRecord, RiskRecord
from signalnoise.repository.postgres_signal_repository import PostgresSignalRepository
from signalnoise.signals.signal_model import Signal

def test_signal_noise_graph():
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

    # 4. Invoke graph app
    initial_state = {
        "query": "delivery blockers",
        "retrieval_results": [],
        "signals": [],
        "trends": [],
        "risks": [],
        "forecasts": [],
        "executive_summary": None
    }

    final_state = graph.app.invoke(initial_state)

    print(final_state)

    # 5. Assertions
    assert len(final_state["retrieval_results"]) > 0
    assert len(final_state["signals"]) > 0
    assert len(final_state["trends"]) > 0
    assert len(final_state["risks"]) > 0
    assert len(final_state["forecasts"]) > 0
    assert final_state["executive_summary"] is not None
    assert final_state["executive_summary"].overall_risk == "Medium"

