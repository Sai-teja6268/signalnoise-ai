import uuid
import os
from datetime import datetime
from signalnoise.document_registry.document_model import DocumentMetadata, ACTIVE
from signalnoise.document_registry.document_repository import DocumentRepository
from signalnoise.document_registry.postgres_document_repository import PostgresDocumentRepository
from signalnoise.utils.hash_util import calculate_file_hash


class DocumentRegistryService:

    def __init__(self, repo: DocumentRepository = None):
        self.repo = repo or PostgresDocumentRepository()

    def register_document(
        self,
        file_path: str,
        chunk_count: int,
        document_type: str = "unknown",
        source: str | None = None
    ) -> DocumentMetadata:
        """
        Calculates hash, generates ID, and registers document metadata in the repository.
        """
        file_hash = calculate_file_hash(file_path)
        file_name = os.path.basename(file_path)
        file_type = os.path.splitext(file_name)[1][1:].lower()
        document_id = str(uuid.uuid4())

        # Determine source if not provided
        if not source:
            lower_name = file_name.lower()
            if "jira" in lower_name:
                source = "jira"
            elif "incident" in lower_name:
                source = "incident"
            elif "meeting" in lower_name:
                source = "meeting_notes"
            elif "support" in lower_name:
                source = "support"
            else:
                source = "unknown"

        document = DocumentMetadata(
            document_id=document_id,
            file_name=file_name,
            file_hash=file_hash,
            file_type=file_type,
            document_type=document_type,
            chunk_count=chunk_count,
            status=ACTIVE,
            ingested_at=datetime.utcnow(),
            source=source
        )

        self.repo.save(document)
        return document

    def check_duplicate(self, file_path: str) -> DocumentMetadata | None:
        """
        Calculates file hash and returns the existing DocumentMetadata if registered.
        """
        file_hash = calculate_file_hash(file_path)
        return self.repo.find_by_hash(file_hash)

    def get_document_by_id(self, document_id: str) -> DocumentMetadata | None:
        return self.repo.find_by_id(document_id)

    def get_all_documents(self) -> list[DocumentMetadata]:
        return self.repo.find_all()

    def get_active_documents(self) -> list[DocumentMetadata]:
        return self.repo.find_active()

    def update_status(self, document_id: str, status: str) -> None:
        self.repo.update_status(document_id, status)
