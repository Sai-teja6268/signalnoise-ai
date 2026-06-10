from signalnoise.citations.citation_builder import (
    CitationBuilder
)

from signalnoise.retrieval.retrieval_result import (
    RetrievalResult
)


def test_citation_builder():

    results = [
        RetrievalResult(
            content="Dependency delay",
            score=0.91,
            confidence=0.88,
            source="meeting_note",
            document_id="1",
            chunk_id="1_chunk_2"
        )
    ]

    builder = CitationBuilder()

    citations = builder.build(
        results
    )

    print()

    for citation in citations:

        print(citation)

    assert len(citations) == 1