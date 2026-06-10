from datetime import datetime
from pydantic import BaseModel

# Document Status Constants
ACTIVE = "ACTIVE"
DELETED = "DELETED"
REINDEXING = "REINDEXING"
FAILED = "FAILED"


class DocumentMetadata(BaseModel):
    document_id: str
    file_name: str
    file_hash: str
    file_type: str
    document_type: str
    chunk_count: int
    status: str
    ingested_at: datetime
    source: str | None = None
