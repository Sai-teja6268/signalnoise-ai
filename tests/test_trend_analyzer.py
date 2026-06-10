from datetime import datetime, timedelta
from signalnoise.history.signal_history import SignalHistory
from signalnoise.history.trend_analyzer import TrendAnalyzer

def test_trend_analyzer_increasing():
    # Previous window (10 days ago): 1 signal
    # Current window (today): 3 signals
    history = [
        SignalHistory(
            signal_type="Dependency Risk",
            confidence=0.7,
            severity="Medium",
            detected_at=datetime.now() - timedelta(days=10)
        ),
        SignalHistory(
            signal_type="Dependency Risk",
            confidence=0.8,
            severity="High",
            detected_at=datetime.now()
        ),
        SignalHistory(
            signal_type="Dependency Risk",
            confidence=0.9,
            severity="High",
            detected_at=datetime.now()
        ),
        SignalHistory(
            signal_type="Dependency Risk",
            confidence=0.9,
            severity="High",
            detected_at=datetime.now()
        )
    ]

    analyzer = TrendAnalyzer()
    trends = analyzer.analyze_trends(history)
    print(trends)
    
    assert len(trends) == 1
    assert trends[0].trend_detection == "Increasing"
    assert trends[0].growth_rate == 200.0


def test_trend_analyzer_decreasing():
    # Previous window (10 days ago): 3 signals
    # Current window (today): 1 signal
    history = [
        SignalHistory(
            signal_type="Dependency Risk",
            confidence=0.7,
            severity="Medium",
            detected_at=datetime.now() - timedelta(days=10)
        ),
        SignalHistory(
            signal_type="Dependency Risk",
            confidence=0.8,
            severity="High",
            detected_at=datetime.now() - timedelta(days=10)
        ),
        SignalHistory(
            signal_type="Dependency Risk",
            confidence=0.9,
            severity="High",
            detected_at=datetime.now() - timedelta(days=10)
        ),
        SignalHistory(
            signal_type="Dependency Risk",
            confidence=0.9,
            severity="High",
            detected_at=datetime.now()
        )
    ]

    analyzer = TrendAnalyzer()
    trends = analyzer.analyze_trends(history)
    
    print(trends)
    assert len(trends) == 1
    assert trends[0].trend_detection == "Decreasing"
    assert trends[0].growth_rate == -66.67


def test_trend_analyzer_stable():
    # Previous window (10 days ago): 2 signals
    # Current window (today): 2 signals
    history = [
        SignalHistory(
            signal_type="Dependency Risk",
            confidence=0.7,
            severity="Medium",
            detected_at=datetime.now() - timedelta(days=10)
        ),
        SignalHistory(
            signal_type="Dependency Risk",
            confidence=0.8,
            severity="High",
            detected_at=datetime.now() - timedelta(days=10)
        ),
        SignalHistory(
            signal_type="Dependency Risk",
            confidence=0.9,
            severity="High",
            detected_at=datetime.now()
        ),
        SignalHistory(
            signal_type="Dependency Risk",
            confidence=0.9,
            severity="High",
            detected_at=datetime.now()
        )
    ]

    analyzer = TrendAnalyzer()
    trends = analyzer.analyze_trends(history)
    
    print(trends)
    assert len(trends) == 1
    assert trends[0].trend_detection == "Stable"
    assert trends[0].growth_rate == 0.0