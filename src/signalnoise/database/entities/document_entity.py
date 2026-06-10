from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import Index

from signalnoise.database.base import Base


class DocumentEntity(Base):
    __tablename__ = "documents"

    document_id = Column(String(100), primary_key=True)

    file_name = Column(String(500), nullable=False)

    file_hash = Column(String(64), unique=True, nullable=False)

    file_type = Column(String(20), nullable=False)

    document_type = Column(String(100), nullable=False)

    chunk_count = Column(Integer, nullable=False)

    status = Column(String(20), nullable=False)

    source = Column(String(100), nullable=False)

    ingested_at = Column(DateTime, nullable=False)

    __table_args__ = (
        Index("idx_document_status", "status"),
        Index("idx_document_type", "document_type"),
        Index("idx_document_source", "source"),
    )

