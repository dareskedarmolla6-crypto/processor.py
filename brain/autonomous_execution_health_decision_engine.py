class AutonomousExecutionHealthDecisionEngine:
    """
    Decides actions from health reports.
    """

    def decide(
        self,
        report
    ):

        if report["health"] == "DEGRADED":

            return {
                "action": "RECOVERY_REQUIRED"
            }


        return {
            "action": "CONTINUE"
        }
