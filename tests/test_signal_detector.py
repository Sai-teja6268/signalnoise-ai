from signalnoise.signals.signal_detector import (
    SignalDetector
)

from signalnoise.retrieval.retrieval_result import (
    RetrievalResult
)


def test_signal_detection():

    detector = SignalDetector()

    results = [

        RetrievalResult(
            content=(
                "Waiting for API dependency. "
                "Testing delayed."
            ),
            score=0.8,
            confidence=0.9,
            source="txt",
            document_id="1",
            chunk_id="1_chunk_0"
        )
    ]

    signals = detector.detect(
        results
    )

    for signal in signals:

        print(signal)

    assert len(signals) > 0