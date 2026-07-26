class InMemoryRuntimeSupervisorMetricsRepository:
    """
    In-memory supervisor metrics storage.
    """

    def __init__(self):
        self._metrics = {}


    def save_metrics(
        self,
        metrics: dict
    ):
        self._metrics = metrics.copy()


    def load_metrics(self):
        return self._metrics.copy()
