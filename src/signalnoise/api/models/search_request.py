from pydantic import BaseModel, Field
from typing import Optional

class SearchRequest(BaseModel):
    query: str = Field(..., description="Query to search organizational documents.")
    document_type: Optional[str] = Field(None, description="Document type filter")
    source: Optional[str] = Field(None, description="Source filter")
