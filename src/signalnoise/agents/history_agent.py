from signalnoise.agents.state import SignalNoiseState
from signalnoise.repository.signal_repository import SignalRepository
from signalnoise.history.signal_history import SignalHistory
from datetime import datetime

class HistoryAgent:
    def __init__(self, repository: SignalRepository):
        self.repository = repository
    
    def _run_history(self, state: SignalNoiseState):
        is_dict = isinstance(state, dict)
        signals = state["signals"] if is_dict else state.signals

        for signal in signals:
            self.repository.save(signal)
        return state

    def __call__(self, state: SignalNoiseState):
        return self._run_history(state)