from abc import ABC, abstractmethod


class RuntimeSupervisorMetricsRepository(ABC):
    """
    Repository contract for supervisor metrics.
    """

    @abstractmethod
    def save_metrics(
        self,
        metrics: dict
    ) -> None:
        pass


    @abstractmethod
    def load_metrics(self) -> dict:
        pass
