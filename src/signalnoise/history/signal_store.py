from signalnoise.history.signal_history import SignalHistory

class SignalStore:
    def __init__(self):
        self.SignalHistory=[]

    def save(self,signal:SignalHistory):
        self.SignalHistory.append(signal)

    def get_all(self):
        return self.SignalHistory

    def get_by_type(self,signal_type:str):
        return [s for s in self.SignalHistory if s.signal_type==signal_type]

    