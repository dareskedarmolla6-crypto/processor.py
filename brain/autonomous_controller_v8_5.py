from brain.risk_adapter import RiskAdapter
from brain.self_correction import SelfCorrection


class AutonomousControllerV8_5:
    """
    FSE Autonomous Controller V8.5

    Full Risk Learning Cycle

    Signal
       ↓
    Decision
       ↓
    Execution Result
       ↓
    Self Correction
       ↓
    Dynamic Risk Update
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


    def run_cycle(self, signals):

        self.cycle += 1

        result = {
            "cycle": self.cycle,
            "decisions": [],
            "trades": [],
            "risk": None,
            "learning": None
        }


        # -------------------------
        # 1. BRAIN
        # -------------------------

        decisions = [
            self.brain.evaluate(x)
            for x in signals
        ]

        result["decisions"] = decisions


        # -------------------------
        # 2. RISK APPROVAL
        # -------------------------

        for item in decisions:

            if item["decision"] != "TRADE":
                continue


            approved = self.governor.approve(
                item["symbol"],
                500,
                "STRONG",
                1000,
                []
            )


            if approved["decision"] != "APPROVED":
                continue


            trade = self.execution.execute(
                {
                    "symbol": item["symbol"],
                    "signal": "BUY",
                    "decision": "TRADE"
                },
                approved,
                size=1,
                entry=50
            )


            result["trades"].append(
                {
                    "symbol": item["symbol"],
                    "trade": trade
                }
            )


        # -------------------------
        # 3. LEARNING + RISK UPDATE
        # -------------------------

        feedback = []

        for trade in result["trades"]:

            feedback.append(
                {
                    "symbol": trade["symbol"],
                    "pnl": 100
                }
            )


        if feedback:

            correction = self.self_correction.analyze(
                feedback
            )

            risk = self.risk_adapter.apply_correction(
                correction
            )

            result["learning"] = correction
            result["risk"] = risk


        return result
