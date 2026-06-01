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
    
    def search(self, query: str):

        dense_results = (
            self.dense_retriever.search(query)
        )

        sparse_results = (
            self.sparse_retriever.search(query)
        )

        return self.rrf_fusion.fuse(
            dense_results,
            sparse_results
        )