class RuntimeSupervisorMetricsAdapter:
    """
    Production supervisor metrics adapter.

    Responsibilities:
        - Translate supervisor lifecycle events
          into metrics updates
        - Keep metrics logic isolated

    Does NOT contain:
        - Runtime control
        - Recovery logic
        - Storage implementation
        - Market logic
    """

    def __init__(
        self,
        metrics
    ):
        self._metrics = metrics


    def record_start(self):
        """
        Record runtime start.
        """

        self._metrics.increment(
            "starts"
        )


    def record_stop(self):
        """
        Record runtime stop.
        """

        self._metrics.increment(
            "stops"
        )


    def record_restart(self):
        """
        Record runtime restart.
        """

        self._metrics.increment(
            "restarts"
        )


    def record_recovery(self):
        """
        Record successful recovery.
        """

        self._metrics.increment(
            "recoveries"
        )


    def record_recovery_failure(self):
        """
        Record failed recovery.
        """

        self._metrics.increment(
            "recovery_failures"
        )


    def snapshot(self) -> dict:
        """
        Return lifecycle metrics snapshot.
        Keeps V10.112 adapter contract stable by filtering core keys.
        """

        snapshot = self._metrics.snapshot()

        return {
            "starts": snapshot.get("starts", 0),
            "stops": snapshot.get("stops", 0),
            "restarts": snapshot.get("restarts", 0),
            "recoveries": snapshot.get("recoveries", 0),
            "recovery_failures": snapshot.get("recovery_failures", 0)
        }
