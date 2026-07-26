from abc import ABC, abstractmethod


class RuntimeMetricsRepository(ABC):
    """
    Production contract for runtime metrics persistence.

    Responsibilities:
        - Store runtime execution metrics
        - Restore runtime execution metrics

    Does NOT contain:
        - Runtime control logic
        - Scheduler logic
        - Market data logic
        - Database implementation
    """

    @abstractmethod
    def save_metrics(
        self,
        metrics: dict
    ) -> None:
        """
        Persist runtime metrics.
        """
        raise NotImplementedError


    @abstractmethod
    def load_metrics(
        self
    ) -> dict:
        """
        Load runtime metrics.
        """
        raise NotImplementedError
