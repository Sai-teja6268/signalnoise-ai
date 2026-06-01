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

def test_hybrid_retrieval():

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

    results = hybrid_retriever.search(
        "delivery blockers"
    )

    assert len(results) > 0

    print("\nHybrid Results\n")

    for rank, (doc, score) in enumerate(
        results,
        start=1
    ):
        print(f"Rank: {rank}")
        print(f"RRF Score: {score}")
        print(
            f"Chunk ID: {doc.chunk_id}"
        )
        print(doc.content)
        print("-" * 50)