class AutonomousExecutionRecoveryStrategyEngine:
    """
    Selects recovery strategy from learned patterns.
    """

    def decide(
        self,
        learning
    ):

        if learning.get("optimized_count", 0) > learning.get("stable_count", 0):

            return {
                "strategy": "ADAPTIVE_RECOVERY"
            }


        if learning.get("stable_count", 0) > 0:

            return {
                "strategy": "STANDARD_RECOVERY"
            }


        return {
            "strategy": "OBSERVE_ONLY"
        }
