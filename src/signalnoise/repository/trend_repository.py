from abc import ABC
from abc import abstractmethod

from signalnoise.trends.trend_model import (
    Trend
)


class TrendRepository(ABC):

    @abstractmethod
    def save(
        self,
        trend: Trend
    ):
        pass

    @abstractmethod
    def get_all(
        self
    ) -> list[Trend]:
        pass

    def count(self):
        pass

    def purge_for_testing(self):
        pass