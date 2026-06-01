from signalnoise.rag.vectorstore import VectorStore
from signalnoise.retrieval.retrieval_result import RetrievalResult

class DenseRetriever:
    def __init__(self):
        self.vectorstore = VectorStore()
    
    def search(self, query:str, k:int=5):
        results = self.vectorstore.similarity_search_with_score(query, k=k)
        retrieved_chunks = []
        for doc, score in results:
            retrieved_chunks.append(
                RetrievalResult(
                    content=doc.page_content,
                    score=score,
                    source=doc.metadata.get("source") or "unknown",
                    document_id=doc.metadata.get("document_id") or "unknown",
                    chunk_id=doc.metadata.get("chunk_id") or "unknown"
                )
            )
        return retrieved_chunks
