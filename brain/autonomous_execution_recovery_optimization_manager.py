class AutonomousExecutionRecoveryOptimizationManager:
    """
    Coordinates recovery analysis and optimization decisions.
    """

    def __init__(
        self,
        intelligence,
        optimizer
    ):

        self.intelligence = intelligence
        self.optimizer = optimizer


    def evaluate(
        self,
        metrics
    ):

        analysis = self.intelligence.analyze(
            metrics
        )

        decision = self.optimizer.optimize(
            analysis
        )

        return {
            "analysis": analysis,
            "decision": decision
        }
