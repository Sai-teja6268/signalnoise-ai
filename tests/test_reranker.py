from signalnoise.services.ingestion_service import (
    IngestionService
)

from signalnoise.ingestion.processor import (
    DocumentProcessor
)

from signalnoise.rag.chunking_service import (
    ChunkingService
)

from signalnoise.retrieval.hybrid_retrieval import (
    HybridRetriever
)

from signalnoise.retrieval.reranker import (
    Reranker
)


def test_reranker():

    ingestion = IngestionService()

    processor = DocumentProcessor()

    chunker = ChunkingService()

    docs = ingestion.ingest(
        "data/sample/meeting_notes.txt"
    )

    lc_docs = processor.process_documents(
        docs
    )

    chunks = chunker.chunk_documents(
        lc_docs
    )

    hybrid_retriever = HybridRetriever(
        chunks
    )

    hybrid_results = hybrid_retriever.search(
        "delivery blockers"
    )

    retrieval_results = [
        result
        for result, _
        in hybrid_results
    ]

    reranker = Reranker()

    reranked_results = reranker.rerank(
        query="delivery blockers",
        results=retrieval_results,
        top_k=5
    )

    print("\n")
    print("=" * 60)
    print("RERANKED RESULTS")
    print("=" * 60)

    for rank, result in enumerate(
        reranked_results,
        start=1
    ):

        print()

        print(f"Rank: {rank}")

        print(
            f"Score: {result.score:.4f}"
        )

        print(
            f"Chunk ID: {result.chunk_id}"
        )

        print(
            f"Document ID: {result.document_id}"
        )

        print(
            f"Source: {result.source}"
        )

        print(
            f"Confidence: {result.confidence:.4f}"
        )

        print()

        print(result.content)

        print("-" * 60)

    assert len(reranked_results) > 0