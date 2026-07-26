from brain.risk_adapter import RiskAdapter
from brain.self_correction import SelfCorrection


class AutonomousControllerV8_3:
    """
    FSE Autonomous Controller V8.3

    Dynamic Risk Injection Cycle
    """

    def __init__(
        self,
        brain,
        allocator,
        governor,
        execution,
        feedback
    ):

        self.brain = brain
        self.allocator = allocator
        self.governor = governor
        self.execution = execution
        self.feedback = feedback

        self.risk_adapter = RiskAdapter()
        self.self_correction = SelfCorrection()

        self.cycle = 0


    def update_risk(self, trades):

        corrections = []

        for trade in trades:

            correction = self.self_correction.analyze(
                [
                    {
                        "symbol": trade["symbol"],
                        "pnl": trade["pnl"]
                    }
                ]
            )

            result = self.risk_adapter.apply_correction(
                correction
            )

            corrections.append(result)

        return corrections
