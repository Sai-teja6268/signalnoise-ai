from signalnoise.retrieval.dense_retriever import (
    DenseRetriever
)

from signalnoise.retrieval.sparse_retriever import (
    SparseRetriever
)

from signalnoise.retrieval.rrf_fusion import (
    RRFfusion
)

class HybridRetriever:
    def __init__(self,chunks):
        self.dense_retriever = DenseRetriever()
        self.sparse_retriever = SparseRetriever(chunks)
        self.rrf_fusion = RRFfusion()
    
    def search(self, query: str, k: int = 5, document_type: str | None = None, source: str | None = None):
        if document_type and document_type.lower().strip() in ("string", "none", ""):
            document_type = None
        if source and source.lower().strip() in ("string", "none", ""):
            source = None

        dense_results = (
            self.dense_retriever.search(query, k=k, document_type=document_type, source=source)
        )

        sparse_results = (
            self.sparse_retriever.search(query, k=k, document_type=document_type, source=source)
        )

        return self.rrf_fusion.fuse(
            dense_results,
            sparse_results
        )