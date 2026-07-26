from .runtime_metrics_repository import RuntimeMetricsRepository


class InMemoryRuntimeMetricsRepository(
    RuntimeMetricsRepository
):
    """
    In-memory runtime metrics persistence.

    Responsibilities:
        - Store metrics during process lifetime
        - Restore metrics snapshot

    Does NOT contain:
        - Runtime control logic
        - Scheduler logic
        - Market data logic
        - Database implementation
    """

    def __init__(self):
        self._metrics = {}

    def save_metrics(
        self,
        metrics: dict
    ) -> None:
        """
        Save metrics snapshot.
        """

        self._metrics = metrics.copy()

    def load_metrics(
        self
    ) -> dict:
        """
        Load metrics snapshot.
        """

        return self._metrics.copy()
