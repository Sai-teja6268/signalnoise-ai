from pydantic import BaseModel

class ConfidenceResult(BaseModel):
    chunk_id: str
    document_id: str
    confidence: float
    explaination: str