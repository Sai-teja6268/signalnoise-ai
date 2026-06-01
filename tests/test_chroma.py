from signalnoise.services.ingestion_service import (
    IngestionService
)

from signalnoise.ingestion.processor import (
    DocumentProcessor
)

from signalnoise.rag.chunking_service import (
    ChunkingService
)

from signalnoise.rag.vectorstore import (
    VectorStore
)
from signalnoise.rag.embedding_service import (
    EMBEDDINGS
)


def test_chroma_storage():

    ingestion = IngestionService()

    processor = DocumentProcessor()

    chunker = ChunkingService()

    vector_store = (
        VectorStore(EMBEDDINGS)
    )

    docs = ingestion.ingest(
        "data/sample/meeting_notes.txt"
    )

    lc_docs = processor.process_documents(docs)

    chunks = chunker.chunk_documents(
        lc_docs
    )

    vector_store.add_documents(
        chunks
    )

    print(
        f"Stored {len(chunks)} chunks"
    )

    assert len(chunks) > 0