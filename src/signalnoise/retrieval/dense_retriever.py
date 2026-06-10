from signalnoise.rag.vectorstore import VectorStore
from signalnoise.retrieval.retrieval_result import RetrievalResult

class DenseRetriever:
    def __init__(self):
        self.vectorstore = VectorStore()
    
    def search(self, query: str, k: int = 5, document_type: str | None = None, source: str | None = None):
        if document_type and document_type.lower().strip() in ("string", "none", ""):
            document_type = None
        if source and source.lower().strip() in ("string", "none", ""):
            source = None

        filters = []
        if document_type:
            filters.append({"document_type": document_type})
        if source:
            filters.append({"source": source})

        filter_dict = None
        if len(filters) == 1:
            filter_dict = filters[0]
        elif len(filters) > 1:
            filter_dict = {"$and": filters}

        results = self.vectorstore.similarity_search_with_score(
            query,
            k=k,
            filter=filter_dict
        )
        retrieved_chunks = []
        for doc, score in results:
            retrieved_chunks.append(
                RetrievalResult(
                    content=doc.page_content,
                    score=score,
                    source=doc.metadata.get("source") or "unknown",
                    document_id=doc.metadata.get("document_id") or "unknown",
                    chunk_id=doc.metadata.get("chunk_id") or "unknown",
                    document_type=doc.metadata.get("document_type") or "unknown"
                )
            )
        return retrieved_chunks
