from signalnoise.services.ingestion_service import (
    IngestionService
)

from signalnoise.ingestion.processor import (
    DocumentProcessor
)

from signalnoise.rag.chunking_service import (
    ChunkingService
)


def test_chunking():

    service = IngestionService()

    docs = service.ingest(
        "data/sample/meeting_notes.txt"
    )

    processor = DocumentProcessor()

    lc_docs = processor.process_documents(docs)

    chunker = ChunkingService()

    chunks = chunker.chunk_documents(lc_docs)

    for index, chunk in enumerate(chunks):
        print(f"\nChunk {index + 1}")
        print(chunk.page_content)
        print(chunk.metadata)

    assert len(chunks) > 0