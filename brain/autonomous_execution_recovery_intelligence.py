class AutonomousExecutionRecoveryIntelligence:
    """
    Analyzes recovery performance.
    """

    def analyze(
        self,
        metrics
    ):

        attempts = metrics.get(
            "attempts",
            0
        )

        success = metrics.get(
            "success",
            0
        )


        if attempts == 0:

            return {
                "status": "NO_DATA"
            }


        rate = success / attempts


        if rate >= 0.8:

            status = "STABLE"

        else:

            status = "NEEDS_IMPROVEMENT"


        return {
            "recovery_rate": rate,
            "status": status
        }
