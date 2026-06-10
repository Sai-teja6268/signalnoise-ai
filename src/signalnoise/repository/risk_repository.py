from abc import ABC
from abc import abstractmethod

from signalnoise.risk.risk_model import Risk


class RiskRepository(ABC):

    @abstractmethod
    def save(
        self,
        risk: Risk
    ):
        pass

    @abstractmethod
    def get_all(
        self
    ) -> list[Risk]:
        pass

    @abstractmethod
    def count(
        self
    ) -> int:
        pass

    @abstractmethod
    def purge_for_testing(
        self
    ):
        pass