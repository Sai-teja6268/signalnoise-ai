from signalnoise.agents.state import (
    SignalNoiseState
)

from signalnoise.agents.retrieval_agent import (
    RetrievalAgent
)

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


def test_retrieval_agent():

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

    retriever = HybridRetriever(
        chunks
    )

    agent = RetrievalAgent(
        retriever
    )

    state: SignalNoiseState = {

        "query": "delivery blockers",

        "retrieval_results": [],

        "signals": [],

        "trends": [],

        "risks": [],

        "executive_summary": None
    }

    updated_state = agent(
        state
    )

    print()

    print(
        f"Retrieved: "
        f"{len(updated_state['retrieval_results'])}"
    )

    assert (
        len(
            updated_state[
                "retrieval_results"
            ]
        )
        > 0
    )