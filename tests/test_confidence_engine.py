from signalnoise.scoring.confidence_engine import (
    ConfidenceEngine
)


def test_confidence_engine():

    engine = ConfidenceEngine()

    confidence = (
        engine.calculate_confidence_score(
            reranker_score=4.2214,
            rrf_score=0.18
        )
    )

    print()

    print(
        f"Confidence: {confidence}"
    )

    assert confidence > 0