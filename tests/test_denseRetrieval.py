from signalnoise.retrieval.dense_retriever import (
    DenseRetrieval
)


def test_dense_retrieval():

    retriever = DenseRetrieval()

    results = retriever.search(
        query="delivery blockers",
        k=5
    )

    print("\n" + "=" * 50)

    print("Test Results")

    print("=" * 50)

    print('\n')

    for idx, result in enumerate(results):

        print(f"Result {idx + 1}")

        print(f"Score: {result.score}")

        print(result.content)

        print(f"Source: {result.source}")
        
        print(f"Document ID: {result.document_id}")

        print(f"Chunk ID: {result.chunk_id}")

        print("-" * 50)

    assert len(results) > 0