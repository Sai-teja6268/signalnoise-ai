from pydantic import BaseModel, Field
from typing import Literal, Optional

class AnalysisRequest(BaseModel):
    query: str = Field(..., description="Query to analyze organizational communications for risks.")
    analysis_mode: Literal["query", "portfolio"] = Field("query", description="Analysis mode: 'query' or 'portfolio'")
    document_type: Optional[str] = Field(None, description="Filter documents by document type")
    source: Optional[str] = Field(None, description="Filter documents by source")

class AnalyzeRequest(AnalysisRequest):
    pass

