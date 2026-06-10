from pydantic import BaseModel

class RetrievalResult(BaseModel):
    content:str
    score: float
    confidence: float = 0.0
    source: str
    document_id: str
    chunk_id: str
    document_type: str | None = None