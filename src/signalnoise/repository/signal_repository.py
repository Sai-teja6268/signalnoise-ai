from abc import ABC
from abc import abstractmethod

from signalnoise.signals.signal_model import (
    Signal
)


class SignalRepository(ABC):

    @abstractmethod
    def save(
        self,
        signal: Signal
    ) -> None:
        pass

    @abstractmethod
    def get_all(
        self
    ) -> list[Signal]:
        pass

    @abstractmethod
    def count(self) -> int:
        pass

    @abstractmethod
    def purge_for_testing(self):
        pass

    @abstractmethod
    def get_by_signal_type(
        self,
        signal_type: str
    ) -> list[Signal]:
        pass