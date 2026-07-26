from brain.portfolio_intelligence import PortfolioIntelligence


class AutonomousControllerV9_3:
    """
    FSE Autonomous Controller V9.3

    Integration:
    - Adaptive Brain
    - Portfolio Intelligence
    - Risk Governor
    - Execution Manager
    """

    def __init__(
        self,
        brain,
        governor,
        execution,
        portfolio=None
    ):

        self.brain = brain
        self.governor = governor
        self.execution = execution

        self.portfolio = (
            portfolio
            if portfolio
            else PortfolioIntelligence()
        )

        self.cycle = 0


    def run_cycle(self, signals):

        self.cycle += 1

        result = {
            "cycle": self.cycle,
            "decisions": [],
            "selected": [],
            "trades": []
        }


        # -------------------------
        # Brain Evaluation
        # -------------------------

        decisions = [
            self.brain.evaluate(signal)
            for signal in signals
        ]

        result["decisions"] = decisions


        # -------------------------
        # Portfolio Selection
        # -------------------------

        selected = self.portfolio.select(
            decisions
        )

        result["selected"] = selected


        # -------------------------
        # Risk + Execution
        # -------------------------

        for item in selected:

            approved = self.governor.approve(
                item["symbol"],
                500,
                "STRONG",
                1000,
                []
            )


            if approved.get("decision") != "APPROVED":
                continue


            trade = self.execution.execute(
                {
                    "symbol": item["symbol"],
                    "signal": item["signal"],
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


        return result
