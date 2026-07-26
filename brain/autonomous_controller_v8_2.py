from brain.dynamic_allocator import DynamicAllocator
from brain.portfolio_rebalancer import PortfolioRebalancer
from brain.portfolio_memory import PortfolioMemory
from brain.risk_adapter import RiskAdapter


class AutonomousControllerV8_2:
    """
    FSE Autonomous Controller V8.2

    Integrated:
    - Brain
    - Dynamic Allocation
    - Portfolio Memory
    - Feedback Learning
    - Risk Adaptation
    """

    def __init__(
        self,
        brain,
        governor,
        execution,
        feedback,
        correction
    ):

        self.brain = brain
        self.allocator = DynamicAllocator()
        self.governor = governor
        self.execution = execution
        self.feedback = feedback
        self.correction = correction

        self.risk_adapter = RiskAdapter()

        self.rebalancer = PortfolioRebalancer()
        self.portfolio_memory = PortfolioMemory()

        self.cycle = 0


    def run_cycle(self, signals):

        self.cycle += 1

        result = {
            "cycle": self.cycle,
            "risk": self.risk_adapter.get_risk(),
            "decisions": [],
            "trades": [],
            "learning": None
        }


        # 1. Brain
        decisions = [
            self.brain.evaluate(s)
            for s in signals
        ]

        result["decisions"] = decisions


        # 2. Trade execution
        for item in decisions:

            if item["decision"] != "TRADE":
                continue


            approved = self.governor.approve(
                item["symbol"],
                500,
                "NORMAL",
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


        # 3. Learning + Risk Update
        if result["trades"]:

            for item in result["trades"]:

                symbol = item["symbol"]

                pnl = 100

                feedback_result = self.feedback.process_trade_result(
                    symbol,
                    pnl
                )


                correction = self.correction.correct(
                    pnl
                )


                self.risk_adapter.apply_correction(
                    correction
                )


            result["learning"] = {
                "risk_after_learning":
                    self.risk_adapter.get_risk()
            }


        return result
