from fastapi.testclient import TestClient
from signalnoise.api.main import app
from signalnoise.database.connection import SessionLocal
from signalnoise.database.models import SignalRecord, TrendRecord, RiskRecord
from signalnoise.repository.postgres_signal_repository import PostgresSignalRepository
from signalnoise.signals.signal_model import Signal
from signalnoise.services.ingestion_service import IngestionService
from signalnoise.ingestion.processor import DocumentProcessor
from signalnoise.rag.chunking_service import ChunkingService
from signalnoise.rag.vectorstore import VectorStore

client = TestClient(app)

def test_api_e2e():
    # 0. Clean database
    session = SessionLocal()
    try:
        session.query(SignalRecord).delete()
        session.query(TrendRecord).delete()
        session.query(RiskRecord).delete()
        session.commit()
    finally:
        session.close()

    # Seed exactly 1 signal so overall risk calculations works
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

    # 1. Ingest and chunk documents into the vector store
    ingestion = IngestionService()
    processor = DocumentProcessor()
    chunker = ChunkingService()

    docs = ingestion.ingest("data/sample/meeting_notes.txt")
    lc_docs = processor.process_documents(docs)
    chunks = chunker.chunk_documents(lc_docs)

    vectorstore = VectorStore()
    try:
        chroma_client = vectorstore.get_vectorstore()
        all_ids = chroma_client.get()["ids"]
        if all_ids:
            chroma_client.delete(ids=all_ids)
    except Exception:
        pass
        
    vectorstore.add_documents(chunks)

    # 2. Invoke the endpoint
    response = client.post(
        "/analyze",
        json={
            "query": "delivery blockers"
        }
    )

    assert response.status_code == 200
    body = response.json()

    assert "query" in body
    assert "retrieval_results" in body
    assert "signals" in body
    assert "trends" in body
    assert "risks" in body
    assert "forecasts" in body
    assert "executive_summary" in body
    
    assert len(body["retrieval_results"]) > 0
    assert len(body["signals"]) > 0
    assert len(body["trends"]) > 0
    assert len(body["risks"]) > 0
    assert len(body["forecasts"]) > 0
    assert body["executive_summary"] is not None
    assert body["executive_summary"]["overall_risk"] == "Medium"
