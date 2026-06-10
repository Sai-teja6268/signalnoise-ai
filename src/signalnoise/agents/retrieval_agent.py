from signalnoise.retrieval.hybrid_retrieval import HybridRetriever
from signalnoise.agents.state import SignalNoiseState
from signalnoise.observability.logger import logger

class RetrievalAgent:
    def __init__(self, retriever: HybridRetriever):
        self.retriever = retriever

    def _run_retrieval(self, state: SignalNoiseState):
        """
        Search Vector Store & Metadata Store
        """
        is_dict = isinstance(state, dict)
        query = state["query"] if is_dict else state.query
        document_type = state.get("document_type") if is_dict else getattr(state, "document_type", None)
        source = state.get("source") if is_dict else getattr(state, "source", None)

        logger.info(
            f"Running retrieval for query: {query} with filters: document_type={document_type}, source={source}"
        )

        results = self.retriever.search(
            query=query,
            k=20,
            document_type=document_type,
            source=source
        )

        flat_results = []
        for doc, score in results:
            doc.score = score
            flat_results.append(doc)

        # Rerank the top 20 retrieved chunks using the Cross Encoder
        from signalnoise.retrieval.reranker import Reranker
        reranker = Reranker()
        reranked_results = reranker.rerank(
            query=query,
            results=flat_results[:20],
            top_k=5
        )

        if is_dict:
            state["retrieval_results"] = reranked_results
        else:
            state.retrieval_results = reranked_results
        return state

    def __call__(self, state: SignalNoiseState):
        return self._run_retrieval(state)
