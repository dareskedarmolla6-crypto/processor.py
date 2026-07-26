class AutonomousExecutionRecoveryDecisionManager:
    """
    Executes recovery decisions.
    """

    def __init__(
        self,
        decision_engine,
        recovery_manager
    ):

        self.decision_engine = decision_engine
        self.recovery_manager = recovery_manager


    def handle(
        self,
        health_report
    ):

        decision = self.decision_engine.decide(
            health_report
        )


        if decision["action"] == "RECOVERY_REQUIRED":

            return self.recovery_manager.recover()


        return {
            "status": "NO_ACTION_REQUIRED"
        }
