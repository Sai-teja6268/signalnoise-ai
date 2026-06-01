from signalnoise.services.ingestion_service import (
    IngestionService
)


service = IngestionService()


def test_csv():

    docs = service.ingest(
        "data/sample/sample.csv"
    )

    assert len(docs) > 0

    print(docs[0])


def test_json():

    docs = service.ingest(
        "data/sample/sample.json"
    )

    assert len(docs) > 0

    print(docs[0])


def test_txt():

    docs = service.ingest(
        "data/sample/sample.txt"
    )

    assert len(docs) > 0

    print(docs[0])