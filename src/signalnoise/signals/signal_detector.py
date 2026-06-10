from signalnoise.signals.signal_model import Signal
from signalnoise.retrieval.retrieval_result import RetrievalResult
from typing import List


class SignalDetector:
    def __init__(self):
        pass
    
    def detect(self, retrieval_results: List[RetrievalResult]) -> Signal:
        signals =[]
        text = " ".join( [result.content.lower() for result in retrieval_results])

        evidence =[
            result.chunk_id
            for result in retrieval_results
        ]

        if("dependency" in text or "blocked" in text):
            signals.append(
                Signal(
                    signal_type="Dependency Risk",
                    severity="High",
                    confidence=0.90,
                    evidence_chunks= evidence,
                    summary=(
                        "Multiple references to"
                        "dependency blockers."
                    )
                )
            )

        if("testing" in text and "delayed" in text):
            signals.append(
                Signal(
                    signal_type="Testing Risk",
                    severity="Medium",
                    confidence=0.80,
                    evidence_chunks= evidence,
                    summary=(
                        "Testing delays detected"
                    )
                )
            )
        return signals
        