class AutonomousExecutionRecoveryLearningEngine:
    """
    Learns from recovery feedback history.
    """

    def learn(
        self,
        history
    ):

        if not history:

            return {
                "status": "NO_HISTORY"
            }


        optimized = sum(
            1
            for item in history
            if item.get("action") == "OPTIMIZE_RECOVERY"
        )


        stable = sum(
            1
            for item in history
            if item.get("action") == "KEEP_CURRENT_STRATEGY"
        )


        return {
            "optimized_count": optimized,
            "stable_count": stable
        }
