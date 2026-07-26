from brain.portfolio_allocator_v9_4 import PortfolioAllocatorV9_4


class AutonomousControllerV9_5:
    """
    FSE Autonomous Controller V9.5

    Integration:
    - Adaptive Brain
    - Portfolio Intelligence
    - Capital Allocation
    - Risk Governor
    - Execution Manager
    """

    def __init__(
        self,
        brain,
        portfolio,
        governor,
        execution,
        allocator=None
    ):

        self.brain = brain
        self.portfolio = portfolio
        self.governor = governor
        self.execution = execution

        self.allocator = (
            allocator
            if allocator
            else PortfolioAllocatorV9_4()
        )

        self.cycle = 0


    def run_cycle(
        self,
        signals
    ):

        self.cycle += 1

        result = {
            "cycle": self.cycle,
            "decisions": [],
            "selected": [],
            "allocations": [],
            "trades": []
        }


        # -------------------------
        # Brain Analysis
        # -------------------------

        decisions = [
            self.brain.evaluate(x)
            for x in signals
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
        # Capital Allocation
        # -------------------------

        allocations = self.allocator.allocate(
            selected
        )

        result["allocations"] = allocations


        # -------------------------
        # Risk + Execution
        # -------------------------

        for item in allocations:

            approved = self.governor.approve(
                item["symbol"],
                item["allocation"],
                "STRONG",
                1000,
                []
            )


            if approved.get(
                "decision"
            ) != "APPROVED":

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
                    "allocation": item["allocation"],
                    "trade": trade
                }
            )


        return result
