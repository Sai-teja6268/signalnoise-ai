from signalnoise.database.connection import SessionLocal
from signalnoise.database.entities.document_entity import DocumentEntity
from signalnoise.document_registry.document_model import DocumentMetadata, ACTIVE
from signalnoise.document_registry.document_repository import DocumentRepository


class PostgresDocumentRepository(DocumentRepository):

    def save(self, document: DocumentMetadata) -> None:
        session = SessionLocal()
        try:
            record = session.query(DocumentEntity).filter(
                DocumentEntity.document_id == document.document_id
            ).first()
            if not record:
                record = DocumentEntity(
                    document_id=document.document_id,
                    file_name=document.file_name,
                    file_hash=document.file_hash,
                    file_type=document.file_type,
                    document_type=document.document_type,
                    chunk_count=document.chunk_count,
                    status=document.status,
                    source=document.source,
                    ingested_at=document.ingested_at
                )
                session.add(record)
            else:
                record.file_name = document.file_name
                record.file_hash = document.file_hash
                record.file_type = document.file_type
                record.document_type = document.document_type
                record.chunk_count = document.chunk_count
                record.status = document.status
                record.source = document.source
                record.ingested_at = document.ingested_at
            session.commit()
        finally:
            session.close()

    def find_by_id(self, document_id: str) -> DocumentMetadata | None:
        session = SessionLocal()
        try:
            record = session.query(DocumentEntity).filter(
                DocumentEntity.document_id == document_id
            ).first()
            if not record:
                return None
            return DocumentMetadata(
                document_id=record.document_id,
                file_name=record.file_name,
                file_hash=record.file_hash,
                file_type=record.file_type,
                document_type=record.document_type,
                chunk_count=record.chunk_count,
                status=record.status,
                source=record.source,
                ingested_at=record.ingested_at
            )
        finally:
            session.close()

    def find_by_hash(self, file_hash: str) -> DocumentMetadata | None:
        session = SessionLocal()
        try:
            record = session.query(DocumentEntity).filter(
                DocumentEntity.file_hash == file_hash
            ).first()
            if not record:
                return None
            return DocumentMetadata(
                document_id=record.document_id,
                file_name=record.file_name,
                file_hash=record.file_hash,
                file_type=record.file_type,
                document_type=record.document_type,
                chunk_count=record.chunk_count,
                status=record.status,
                source=record.source,
                ingested_at=record.ingested_at
            )
        finally:
            session.close()

    def find_all(self) -> list[DocumentMetadata]:
        session = SessionLocal()
        try:
            records = session.query(DocumentEntity).all()
            return [
                DocumentMetadata(
                    document_id=record.document_id,
                    file_name=record.file_name,
                    file_hash=record.file_hash,
                    file_type=record.file_type,
                    document_type=record.document_type,
                    chunk_count=record.chunk_count,
                    status=record.status,
                    source=record.source,
                    ingested_at=record.ingested_at
                )
                for record in records
            ]
        finally:
            session.close()

    def find_active(self) -> list[DocumentMetadata]:
        session = SessionLocal()
        try:
            records = session.query(DocumentEntity).filter(
                DocumentEntity.status == ACTIVE
            ).all()
            return [
                DocumentMetadata(
                    document_id=record.document_id,
                    file_name=record.file_name,
                    file_hash=record.file_hash,
                    file_type=record.file_type,
                    document_type=record.document_type,
                    chunk_count=record.chunk_count,
                    status=record.status,
                    source=record.source,
                    ingested_at=record.ingested_at
                )
                for record in records
            ]
        finally:
            session.close()

    def update_status(self, document_id: str, status: str) -> None:
        session = SessionLocal()
        try:
            record = session.query(DocumentEntity).filter(
                DocumentEntity.document_id == document_id
            ).first()
            if record:
                record.status = status
                session.commit()
        finally:
            session.close()

    def exists(self, file_hash: str) -> bool:
        session = SessionLocal()
        try:
            count = session.query(DocumentEntity).filter(
                DocumentEntity.file_hash == file_hash
            ).count()
            return count > 0
        finally:
            session.close()
