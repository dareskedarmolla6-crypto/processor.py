class AutonomousExecutionRecoveryOptimizationEngine:
    """
    Decides recovery optimization actions.
    """

    def optimize(
        self,
        analysis
    ):

        if analysis["status"] == "NEEDS_IMPROVEMENT":

            return {
                "action": "OPTIMIZE_RECOVERY"
            }


        if analysis["status"] == "STABLE":

            return {
                "action": "KEEP_CURRENT_STRATEGY"
            }


        return {
            "action": "COLLECT_MORE_DATA"
        }
