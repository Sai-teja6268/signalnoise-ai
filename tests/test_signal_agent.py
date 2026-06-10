from signalnoise.agents.signal_agent import (
    SignalAgent
)

from signalnoise.signals.signal_detector import (
    SignalDetector
)

from signalnoise.retrieval.retrieval_result import (
    RetrievalResult
)


def test_signal_agent():

    state = {

        "query": "delivery blockers",

        "retrieval_results": [

            RetrievalResult(
                content=(
                    "Waiting for API dependency. "
                    "Testing delayed."
                ),
                score=0.9,
                confidence=0.8,
                source="txt",
                document_id="1",
                chunk_id="1_chunk_0"
            )

        ],

        "signals": [],

        "trends": [],

        "risks": [],

        "executive_summary": None
    }

    agent = SignalAgent(
        SignalDetector()
    )

    updated_state = agent(
        state
    )

    print()

    print(
        updated_state["signals"]
    )

    assert (
        len(
            updated_state["signals"]
        )
        > 0
    )