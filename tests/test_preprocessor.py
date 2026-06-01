from signalnoise.services.ingestion_service import (
    IngestionService
)

from signalnoise.ingestion.processor import (
    DocumentProcessor
)


def test_document_processor():

    service = IngestionService()

    docs = service.ingest(
        "data/sample/sample.txt"
    )

    processor = DocumentProcessor()

    langchain_docs = processor.process_documents(docs)

    assert len(langchain_docs) > 0

    print(langchain_docs[0])