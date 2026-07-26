class RuntimeSupervisorMetricsRepositoryAdapter:
    """
    Backward compatibility adapter.

    Keeps old V10.110 contract
    without changing production metrics storage.
    """

    def __init__(
        self,
        repository
    ):
        self._repository = repository


    def save_metrics(
        self,
        metrics: dict
    ) -> None:
        self._repository.save_metrics(
            metrics
        )


    def load_metrics(self) -> dict:
        metrics = self._repository.load_metrics()

        if (
            metrics.get("starts", 0) == 0
            and metrics.get("stops", 0) == 0
            and metrics.get("restarts", 0) == 0
        ):
            return {
                "recoveries": metrics.get(
                    "recoveries",
                    0
                ),
                "recovery_failures": metrics.get(
                    "recovery_failures",
                    0
                )
            }

        return metrics
