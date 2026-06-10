from abc import ABC, abstractmethod

class BaseSignal(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def detect(self, *args, **kwargs):
        """
        Detect signals of risk in the input data.
        """
        pass
