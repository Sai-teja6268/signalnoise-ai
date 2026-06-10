import pytest
from signalnoise.database.connection import SessionLocal
from signalnoise.database.entities.document_entity import DocumentEntity


@pytest.fixture(autouse=True)
def clean_documents_table():
    # Purge before test
    session = SessionLocal()
    try:
        session.query(DocumentEntity).delete()
        session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()

    yield

    # Purge after test
    session = SessionLocal()
    try:
        session.query(DocumentEntity).delete()
        session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()
