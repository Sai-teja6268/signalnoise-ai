from pydantic import BaseModel

class RetrievalResult(BaseModel):
    content:str
    score: float
    source: str
    document_id: str
    chunk_id: str