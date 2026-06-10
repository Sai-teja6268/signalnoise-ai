from sentence_transformers import CrossEncoder
from signalnoise.retrieval.retrieval_result import RetrievalResult
from typing import List
from math import exp
from signalnoise.scoring.confidence_engine import ConfidenceEngine

class Reranker:
    def __init__(self, model_path="cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.reranker=CrossEncoder(model_path)
        self.confidence_engine = ConfidenceEngine()
    
    def rerank(self, query:str, results:List[RetrievalResult],top_k:int=5) -> list[RetrievalResult]:

        if not results:
            return []

        pairs=[
            (query,result.content) for result in results
        ]

        scores = self.reranker.predict(pairs)

        reranked_results=[]

        for doc, score in zip(results, scores):
            confidence = (
                self.confidence_engine
                .calculate_confidence_score(
                    reranker_score=score
                )
            )
            reranked_results.append(
                RetrievalResult(
                    content=doc.content,
                    score=float(score), 
                    confidence=confidence,
                    source=doc.source,
                    document_id=doc.document_id,
                    chunk_id=doc.chunk_id,
                    document_type=doc.document_type
                )
            )

        reranked_results.sort(key=lambda x:x.score, reverse=True)

        return reranked_results[:top_k]
        
    