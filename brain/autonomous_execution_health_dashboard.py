class AutonomousExecutionHealthDashboard:
    """
    Builds execution health reports.
    """

    def __init__(
        self,
        observability
    ):

        self.observability = observability


    def report(self):

        snapshot = self.observability.snapshot()

        metrics = snapshot["metrics"]

        state = snapshot["state"]


        return {
            "health": "HEALTHY"
            if metrics.get("failure", 0) == 0
            else "DEGRADED",
            "metrics": metrics,
            "state": state,
            "events": len(snapshot["events"])
        }
