from typing import Any
from signalnoise.agents.state import SignalNoiseState
from signalnoise.signals.llm_signal_detector import LLMSignalDetector
from signalnoise.observability.logger import logger

class SignalAgent:
    def __init__(self, signal_detector: Any):
        self.signal_detector = signal_detector

    def _run_signals(self, state: SignalNoiseState):
        """
        Detect Signals in the retrieved results
        """
        is_dict = isinstance(state, dict)
        retrieval_results = state["retrieval_results"] if is_dict else state.retrieval_results
        user_query = state["query"] if is_dict else getattr(state, "query", None)

        combined_text = "\n\n".join(
            result.content for result in retrieval_results
        )

        if isinstance(self.signal_detector, LLMSignalDetector):
            detector_output = self.signal_detector.detect(
                query=combined_text,
                user_query=user_query
            )
            if isinstance(detector_output, list):
                signals = detector_output
            else:
                signals = [detector_output]
        else:
            signals = self.signal_detector.detect(
                retrieval_results
            )

        logger.info(
            f"Detected {len(signals)} signals"
        )

        if is_dict:
            state["signals"] = signals
        else:
            state.signals = signals
        return state


    def __call__(self, state: SignalNoiseState):
        return self._run_signals(state)
    