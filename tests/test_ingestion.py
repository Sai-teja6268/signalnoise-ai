import pytest
from signalnoise.database.connection import SessionLocal
from signalnoise.database.entities.document_entity import DocumentEntity
from signalnoise.services.ingestion_service import IngestionService


service = IngestionService()


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


def test_csv():
    docs = service.ingest("data/sample/sample.csv")
    assert isinstance(docs, list)
    assert len(docs) > 0

    # Test duplicate check on second ingest
    dup = service.ingest("data/sample/sample.csv")
    assert isinstance(dup, dict)
    assert dup["message"] == "Document already exists"
    assert "document_id" in dup


def test_json():
    docs = service.ingest("data/sample/sample.json")
    assert isinstance(docs, list)
    assert len(docs) > 0

    # Test duplicate check on second ingest
    dup = service.ingest("data/sample/sample.json")
    assert isinstance(dup, dict)
    assert dup["message"] == "Document already exists"
    assert "document_id" in dup


def test_txt():
    docs = service.ingest("data/sample/sample.txt")
    assert isinstance(docs, list)
    assert len(docs) > 0

    # Test duplicate check on second ingest
    dup = service.ingest("data/sample/sample.txt")
    assert isinstance(dup, dict)
    assert dup["message"] == "Document already exists"
    assert "document_id" in dup


def test_ingest_with_explicit_valid_overrides():
    purge_documents()
    docs = service.ingest("data/sample/sample.txt", source="slack", document_type="security")
    assert isinstance(docs, list)
    assert len(docs) > 0
    
    # Retrieve the registered document
    session = SessionLocal()
    try:
        from signalnoise.database.entities.document_entity import DocumentEntity
        doc_entity = session.query(DocumentEntity).filter_by(file_name="sample.txt").first()
        assert doc_entity is not None
        assert doc_entity.source == "slack"
        assert doc_entity.document_type == "security"
    finally:
        session.close()


def test_ingest_with_explicit_invalid_overrides_raises_value_error():
    purge_documents()
    with pytest.raises(ValueError) as excinfo:
        service.ingest("data/sample/sample.txt", source="invalid_source_name")
    assert "Invalid source" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        service.ingest("data/sample/sample.txt", document_type="invalid_doc_type")
    assert "Invalid document_type" in str(excinfo.value)


def test_ingest_with_placeholder_overrides_triggers_autodetect():
    purge_documents()
    # "string" and "none" should be treated as None and trigger auto-detection
    docs = service.ingest("data/sample/sample.txt", source="string", document_type="none")
    assert isinstance(docs, list)
    assert len(docs) > 0
    
    session = SessionLocal()
    try:
        from signalnoise.database.entities.document_entity import DocumentEntity
        doc_entity = session.query(DocumentEntity).filter_by(file_name="sample.txt").first()
        assert doc_entity is not None
        # Should not be "string" or "none"
        assert doc_entity.source != "string"
        assert doc_entity.document_type != "none"
        assert doc_entity.source in ["unknown", "support", "incident", "meeting_notes", "jira", "confluence", "slack", "email"]
        assert doc_entity.document_type in ["unknown", "support", "incident", "retrospective", "delivery", "compliance", "security", "operations"]
    finally:
        session.close()