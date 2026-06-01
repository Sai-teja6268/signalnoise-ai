from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from typing import List, Optional
from signalnoise.retrieval.retrieval_result import RetrievalResult

class SparseRetriever:

    def __init__(
        self,
        documents: List[Document],
        k: int = 5
    ):

        self.retriever = (
            BM25Retriever.from_documents(
                documents
            )
        )

        self.retriever.k = k

    def search(
        self,
        query: str
    ) -> List[RetrievalResult]:

        results = self.retriever.invoke(
            query
        )
        retrieved_chunks = []
        for rank,doc in enumerate(results,1):
            retrieved_chunks.append(
                RetrievalResult(
                    content=doc.page_content,
                    score=1.0/ rank,
                    source=doc.metadata.get("source") or "unknown",
                    document_id=doc.metadata.get("document_id") or "unknown",
                    chunk_id=doc.metadata.get("chunk_id") or "unknown"
                )
            )
        return retrieved_chunks 