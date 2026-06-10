from signalnoise.trends.trend_detector import (
    TrendDetector
)

from signalnoise.signals.signal_model import (
    Signal
)

from signalnoise.trends.trend_model import (
    Trend
)

def test_trend_detection():

    signals = [

        Signal(
            signal_type="Dependency Risk",
            severity="High",
            confidence=0.9,
            evidence_chunks=["1"],
            summary="..."
        ),

        Signal(
            signal_type="Dependency Risk",
            severity="High",
            confidence=0.9,
            evidence_chunks=["2"],
            summary="..."
        ),

        Signal(
            signal_type="Dependency Risk",
            severity="High",
            confidence=0.9,
            evidence_chunks=["3"],
            summary="..."
        )
    ]

    detector = TrendDetector()

    trends = detector.detect_trends(
        signals
    )

    print(trends)

    assert len(trends) > 0