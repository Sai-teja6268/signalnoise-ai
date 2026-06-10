import pytest
from fastapi.testclient import TestClient
from signalnoise.api.main import app
from unittest.mock import MagicMock
from signalnoise.api.routers.analyze import get_signalnoise_service
from signalnoise.database.connection import SessionLocal
from signalnoise.database.entities.document_entity import DocumentEntity

client = TestClient(app)


def purge_documents():
    session = SessionLocal()
    try:
        session.query(DocumentEntity).delete()
        session.commit()
    finally:
        session.close()


@pytest.fixture(autouse=True)
def setup_teardown():
    purge_documents()
    yield
    purge_documents()


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "SignalNoiseAI is running"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_version_check():
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {
        "service": "signalnoise-ai",
        "version": "1.0.0"
    }

def test_get_signals():
    response = client.get("/signals")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_trends():
    response = client.get("/trends")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_risks():
    response = client.get("/risks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_forecasts():
    response = client.get("/forecasts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_analyze_endpoint():
    # Mock the SignalNoiseService
    mock_service = MagicMock()
    mock_service.analyze.return_value = {
        "query": "delivery blockers",
        "retrieval_results": [],
        "signals": [],
        "trends": [],
        "risks": [],
        "forecasts": [],
        "executive_summary": {
            "overall_risk": "Low",
            "key_risks": [],
            "forecast_outlook": "No forecast available",
            "summary": "No risks detected"
        }
    }
    
    # Override dependency
    app.dependency_overrides[get_signalnoise_service] = lambda: mock_service
    
    try:
        response = client.post("/analyze", json={"query": "delivery blockers"})
        assert response.status_code == 200
        data = response.json()
        assert data["query"] == "delivery blockers"
        assert data["executive_summary"]["overall_risk"] == "Low"
    finally:
        # Clean up dependency override
        app.dependency_overrides.clear()

def test_ingest_document_and_read_apis():
    # 1. Initially registry should be empty
    response = client.get("/documents")
    assert response.status_code == 200
    assert response.json() == []

    # 2. Ingest document
    file_path = "data/sample/meeting_notes.txt"
    with open(file_path, "rb") as f:
        response = client.post(
            "/documents/ingest",
            files={"file": ("meeting_notes.txt", f, "text/plain")}
        )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

    # 3. Read documents API -> should return 1 document metadata
    response = client.get("/documents")
    assert response.status_code == 200
    docs = response.json()
    assert len(docs) == 1
    doc = docs[0]
    assert doc["file_name"] == "meeting_notes.txt"
    assert doc["status"] == "ACTIVE"
    assert doc["source"] == "meeting_notes"
    doc_id = doc["document_id"]

    # 4. Read document by ID
    response = client.get(f"/documents/{doc_id}")
    assert response.status_code == 200
    assert response.json()["document_id"] == doc_id

    # 5. Read non-existent document by ID -> should return 404
    response = client.get("/documents/non-existent-id")
    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found"

    # 6. Ingest same document again -> should get duplicate check message
    with open(file_path, "rb") as f:
        response = client.post(
            "/documents/ingest",
            files={"file": ("meeting_notes.txt", f, "text/plain")}
        )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Document already exists"
    assert data["document_id"] == doc_id


def test_analyze_endpoint_with_mode():
    mock_service = MagicMock()
    mock_service.analyze.return_value = {
        "query": "delivery blockers",
        "retrieval_results": [],
        "signals": [],
        "trends": [],
        "risks": [],
        "forecasts": [],
        "executive_summary": {
            "overall_risk": "Low",
            "key_risks": [],
            "forecast_outlook": "No forecast available",
            "summary": "No risks detected"
        },
        "historical_analysis": False
    }
    
    app.dependency_overrides[get_signalnoise_service] = lambda: mock_service
    
    try:
        response = client.post("/analyze", json={"query": "delivery blockers", "analysis_mode": "query"})
        assert response.status_code == 200
        mock_service.analyze.assert_called_once_with(
            query="delivery blockers",
            analysis_mode="query",
            document_type=None,
            source=None
        )
    finally:
        app.dependency_overrides.clear()


def test_executive_summary_endpoint():
    from signalnoise.repository.postgres_risk_repository import PostgresRiskRepository
    risk_repo = PostgresRiskRepository()
    risk_repo.purge_for_testing()
    
    # Empty state test
    response = client.get("/executive-summary")
    assert response.status_code == 200
    data = response.json()
    assert data["overall_risk"] == "Low"
    assert data["top_risks"] == []
    assert data["forecast"] == "No forecast available"
    assert data["summary"] == "No risks detected"

    # Seeded state test
    from signalnoise.risk.risk_model import Risk
    risk_repo.save(
        Risk(
            signal_type="Dependency Risk",
            risk_score=75.0,
            severity="Medium",
            explanation="Some dependency concerns"
        )
    )
    
    try:
        response = client.get("/executive-summary")
        assert response.status_code == 200
        data = response.json()
        assert data["overall_risk"] == "Medium"
        assert "Dependency Risk (Medium)" in data["top_risks"]
        assert data["forecast"] == "Monitor closely and mitigate"
        assert "Highest risk detected: Dependency Risk" in data["summary"]
    finally:
        risk_repo.purge_for_testing()


def test_metadata_aware_retrieval_validation():
    session = SessionLocal()
    from signalnoise.database.models import SignalRecord, TrendRecord, RiskRecord
    from signalnoise.database.entities.document_entity import DocumentEntity
    from signalnoise.rag.vectorstore import VectorStore
    
    try:
        session.query(SignalRecord).delete()
        session.query(TrendRecord).delete()
        session.query(RiskRecord).delete()
        session.query(DocumentEntity).delete()
        session.commit()
    finally:
        session.close()
        
    vectorstore = VectorStore()
    try:
        chroma_client = vectorstore.get_vectorstore()
        all_ids = chroma_client.get()["ids"]
        if all_ids:
            chroma_client.delete(ids=all_ids)
    except Exception:
        pass
        
    import os
    os.makedirs("data/test_samples", exist_ok=True)
    
    files_to_create = {
        "data/test_samples/customer_complaints_support.txt": "customer complaints weekly report, support team details",
        "data/test_samples/production_outage_incident.txt": "production outage incident report, billing service outage",
        "data/test_samples/team_burnout_retro.txt": "team burnout retrospective notes, engineers overloaded",
        "data/test_samples/dependency_blocker_delivery.txt": "dependency blocker weekly status, payments team blocked"
    }
    
    for path, content in files_to_create.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
            
    from signalnoise.services.ingestion_service import IngestionService
    ingestion = IngestionService()
    for path in files_to_create.keys():
        ingestion.ingest(path)
        
    try:
        from signalnoise.retrieval.hybrid_retrieval import HybridRetriever
        from langchain_core.documents import Document
        
        # Load ingested documents to initialize BM25 sparse index
        data = chroma_client.get()
        documents = []
        if data and "documents" in data:
            for content, metadata in zip(data["documents"], data["metadatas"]):
                documents.append(Document(page_content=content, metadata=metadata or {}))
                
        retriever = HybridRetriever(documents)
        results = retriever.search(
            query="customer complaints",
            k=20,
            document_type="support"
        )
        
        assert len(results) > 0
        for doc, score in results:
            assert doc.document_type == "support"
            assert "support" in doc.source or "support" in doc.chunk_id or "support" in doc.content
    finally:
        for path in files_to_create.keys():
            if os.path.exists(path):
                os.remove(path)
        if os.path.exists("data/test_samples"):
            os.rmdir("data/test_samples")


def test_metadata_aware_retrieval_placeholders():
    from signalnoise.retrieval.hybrid_retrieval import HybridRetriever
    from langchain_core.documents import Document

    docs = [
        Document(page_content="doc support", metadata={"document_type": "support", "source": "jira", "document_id": "1", "chunk_id": "1"}),
        Document(page_content="doc retro", metadata={"document_type": "retrospective", "source": "slack", "document_id": "2", "chunk_id": "2"}),
    ]

    retriever = HybridRetriever(docs)

    # Passing placeholder values should not crash or return empty results due to strict match on "string"
    results = retriever.search(
        query="doc",
        k=2,
        document_type="support",
        source="string"
    )

    # Since "source" is placeholder "string", it gets normalized to None, so it shouldn't filter by source.
    # Therefore, we should still retrieve the support doc (since document_type="support" is matched).
    assert len(results) > 0
    assert any(doc.document_type == "support" for doc, _ in results)





