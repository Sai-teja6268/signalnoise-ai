from signalnoise.services.ingestion_service import (
    IngestionService
)

from signalnoise.ingestion.processor import (
    DocumentProcessor
)

from signalnoise.rag.chunking_service import (
    ChunkingService
)

from signalnoise.retrieval.sparse_retriever import (
    SparseRetriever
)


def test_sparse_retrieval():

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

    retriever = SparseRetriever(
        chunks
    )

    results = retriever.search(
        "API dependency"
    )

    print()

    for idx, doc in enumerate(results):

        print(
            f"Result {idx + 1}"
        )

        print(doc.content)

        print(f"Source: {doc.source}, Document ID: {doc.document_id}, Chunk ID: {doc.chunk_id}")

        print("-" * 50)

    assert len(results) > 0