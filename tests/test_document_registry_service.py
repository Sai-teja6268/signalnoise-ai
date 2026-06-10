import os
import tempfile
from datetime import datetime
import pytest
from signalnoise.database.connection import SessionLocal
from signalnoise.database.entities.document_entity import DocumentEntity
from signalnoise.document_registry.document_model import (
    DocumentMetadata,
    ACTIVE,
    DELETED,
    REINDEXING
)
from signalnoise.document_registry.document_service import DocumentRegistryService


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


def test_document_registry_service_flow():
    service = DocumentRegistryService()

    # Create a dummy file for registration
    with tempfile.NamedTemporaryFile(suffix="_incident_report.pdf", mode="wb", delete=False) as f:
        f.write(b"mock document content")
        f.flush()
        file_path = f.name

    try:
        # 1. Verify initially not a duplicate
        existing = service.check_duplicate(file_path)
        assert existing is None

        # 2. Register document
        doc = service.register_document(
            file_path=file_path,
            chunk_count=5,
            document_type="incident"
        )
        assert doc.document_id is not None
        assert doc.file_name == os.path.basename(file_path)
        assert doc.chunk_count == 5
        assert doc.document_type == "incident"
        assert doc.status == ACTIVE
        assert doc.source == "incident"  # derived from filename!

        # 3. Check duplicate again -> should find it
        existing = service.check_duplicate(file_path)
        assert existing is not None
        assert existing.document_id == doc.document_id

        # 4. Check find by ID
        found = service.get_document_by_id(doc.document_id)
        assert found is not None
        assert found.document_id == doc.document_id

        # 5. Check active/all list
        assert len(service.get_all_documents()) == 1
        assert len(service.get_active_documents()) == 1

        # 6. Check update status
        service.update_status(doc.document_id, REINDEXING)
        found = service.get_document_by_id(doc.document_id)
        assert found.status == REINDEXING

    finally:
        os.remove(file_path)
