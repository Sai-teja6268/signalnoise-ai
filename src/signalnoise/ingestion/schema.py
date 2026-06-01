from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class EnterpriseDocument(BaseModel):
    document_id: str
    source: str
    content: str

    file_name: Optional[str] = None
    team: Optional[str] = None
    department: Optional[str] = None
    date: Optional[str] = None

    metadata: dict = Field(default_factory=dict)

    ingestion_timestamp: datetime = Field(
        default_factory=datetime.utcnow
    )