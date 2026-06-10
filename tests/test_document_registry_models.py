from datetime import datetime
from signalnoise.document_registry.document_model import (
    DocumentMetadata,
    ACTIVE,
    DELETED,
    REINDEXING,
    FAILED
)
from signalnoise.database.entities.document_entity import DocumentEntity


def test_status_constants():
    assert ACTIVE == "ACTIVE"
    assert DELETED == "DELETED"
    assert REINDEXING == "REINDEXING"
    assert FAILED == "FAILED"


def test_document_metadata_model():
    now = datetime.utcnow()
    metadata = DocumentMetadata(
        document_id="doc_123",
        file_name="jira_export.csv",
        file_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        file_type="csv",
        document_type="jira",
        chunk_count=10,
        status=ACTIVE,
        ingested_at=now,
        source="jira"
    )

    assert metadata.document_id == "doc_123"
    assert metadata.file_name == "jira_export.csv"
    assert metadata.file_hash == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert metadata.file_type == "csv"
    assert metadata.document_type == "jira"
    assert metadata.chunk_count == 10
    assert metadata.status == ACTIVE
    assert metadata.ingested_at == now
    assert metadata.source == "jira"


def test_document_entity_model():
    assert DocumentEntity.__tablename__ == "documents"

    now = datetime.utcnow()
    entity = DocumentEntity(
        document_id="doc_123",
        file_name="jira_export.csv",
        file_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        file_type="csv",
        document_type="jira",
        chunk_count=10,
        status=ACTIVE,
        source="jira",
        ingested_at=now
    )

    assert entity.document_id == "doc_123"
    assert entity.file_name == "jira_export.csv"
    assert entity.file_hash == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert entity.file_type == "csv"
    assert entity.document_type == "jira"
    assert entity.chunk_count == 10
    assert entity.status == ACTIVE
    assert entity.source == "jira"
    assert entity.ingested_at == now
