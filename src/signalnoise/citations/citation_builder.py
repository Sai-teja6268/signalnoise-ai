from typing import List
from signalnoise.citations.citation_results import (
    Citation
)
from signalnoise.retrieval.retrieval_result import RetrievalResult

class CitationBuilder():
    def build(self,results:list[RetrievalResult])->list[Citation]:
        citations = []
        for doc in results:
            citations.append(
                Citation(
                    document_id=doc.document_id,
                    chunk_id=doc.chunk_id,
                    source=doc.source,
                    confidence=doc.confidence
                )
            )
        return citations