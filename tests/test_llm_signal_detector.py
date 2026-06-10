from signalnoise.signals.llm_signal_detector import (
    LLMSignalDetector
)


def test_llm_signal_detector():

    detector = (
        LLMSignalDetector()
    )

    text = """
Teams are waiting for an API
dependency from another team.

Testing activities have been
delayed.

Release timelines may slip.
"""

    result = detector.detect(
        text
    )

    print()

    print(result)

    assert result is not None


def test_llm_signal_detector_query_focus():
    detector = LLMSignalDetector()
    
    mixed_text = """
Payments team is waiting for an API dependency from Customer Profile team.
Testing activities are delayed.

Engineering team retro:
Multiple engineers reported burnout due to long hours.
Two senior developers have resigned this quarter.
"""
    
    result = detector.detect(mixed_text, user_query="dependency issue")
    
    assert len(result) > 0
    signal_types = [sig.signal_type.lower() for sig in result]
    
    assert any("depend" in t for t in signal_types)
    assert not any("resource" in t or "burnout" in t or "morale" in t or "staff" in t for t in signal_types)