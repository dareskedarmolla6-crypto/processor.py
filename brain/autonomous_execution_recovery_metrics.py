class AutonomousExecutionRecoveryMetrics:
    """
    Tracks recovery performance.
    """

    def __init__(self):

        self._metrics = {
            "attempts": 0,
            "success": 0,
            "failure": 0
        }


    def record(
        self,
        result
    ):

        self._metrics["attempts"] += 1

        if result.get("status") == "RECOVERED":

            self._metrics["success"] += 1

        else:

            self._metrics["failure"] += 1



    def snapshot(self):

        return dict(self._metrics)
