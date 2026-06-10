from datetime import datetime
import pytest
from signalnoise.database.connection import SessionLocal
from signalnoise.database.entities.document_entity import DocumentEntity
from signalnoise.document_registry.document_model import (
    DocumentMetadata,
    ACTIVE,
    DELETED
)
from signalnoise.document_registry.postgres_document_repository import (
    PostgresDocumentRepository
)


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


def test_postgres_document_repository_lifecycle():
    repo = PostgresDocumentRepository()
    
    # 1. Test exists on non-existent hash
    dummy_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert not repo.exists(dummy_hash)
    assert repo.find_by_hash(dummy_hash) is None
    assert repo.find_by_id("doc_1") is None

    # 2. Test save new document
    now = datetime.utcnow().replace(microsecond=0)
    doc = DocumentMetadata(
        document_id="doc_1",
        file_name="jira_export.csv",
        file_hash=dummy_hash,
        file_type="csv",
        document_type="jira",
        chunk_count=10,
        status=ACTIVE,
        source="jira",
        ingested_at=now
    )
    repo.save(doc)

    # 3. Test exists and find
    assert repo.exists(dummy_hash)
    
    found_by_id = repo.find_by_id("doc_1")
    assert found_by_id is not None
    assert found_by_id.document_id == "doc_1"
    assert found_by_id.file_name == "jira_export.csv"
    assert found_by_id.file_hash == dummy_hash
    assert found_by_id.file_type == "csv"
    assert found_by_id.document_type == "jira"
    assert found_by_id.chunk_count == 10
    assert found_by_id.status == ACTIVE
    assert found_by_id.source == "jira"
    assert found_by_id.ingested_at == now

    found_by_hash = repo.find_by_hash(dummy_hash)
    assert found_by_hash is not None
    assert found_by_hash.document_id == "doc_1"

    # 4. Test find_all and find_active
    all_docs = repo.find_all()
    assert len(all_docs) == 1
    assert all_docs[0].document_id == "doc_1"

    active_docs = repo.find_active()
    assert len(active_docs) == 1
    assert active_docs[0].document_id == "doc_1"

    # 5. Test update_status
    repo.update_status("doc_1", DELETED)
    updated_doc = repo.find_by_id("doc_1")
    assert updated_doc is not None
    assert updated_doc.status == DELETED

    # Now it should not be active
    assert len(repo.find_active()) == 0
    assert len(repo.find_all()) == 1  # but it still exists in find_all (audit trail!)
