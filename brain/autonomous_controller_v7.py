from brain.portfolio_rebalancer import PortfolioRebalancer
from brain.portfolio_rebalancer import PortfolioRebalancer
from brain.dynamic_allocator import DynamicAllocator
from brain.portfolio_memory import PortfolioMemory

class AutonomousControllerV7:
    """
    FSE Autonomous Controller V7.6
    Integrated with PortfolioMemory batch update cycle
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
        self.allocator = DynamicAllocator()
        self.governor = governor
        self.execution = execution
        self.feedback = feedback

        self.rebalancer = PortfolioRebalancer()
        self.portfolio_memory = PortfolioMemory()

        self.cycle = 0
        self.history = []

    def run_cycle(self, signals):
        self.cycle += 1
        result = {
            "cycle": self.cycle,
            "decisions": [],
            "allocations": [],
            "trades": [],
            "learning": None
        }

        # -------------------------
        # 1. BRAIN
        # -------------------------
        decisions = [self.brain.evaluate(s) for s in signals]
        result["decisions"] = decisions

        # -------------------------
        # 2. CAPITAL & REBALANCE
        # -------------------------
        opportunities = [x for x in decisions if x["decision"] == "TRADE"]

        # Optimize brain state ONCE
        brain_state = self.brain.optimizer.optimize()

        if opportunities:
            assets = []
            for item in opportunities:
                report = brain_state["report"].get(item["symbol"], {})
                assets.append({
                    "symbol": item["symbol"],
                    "score": report.get("score", item["confidence"] * 100),
                    "status": report.get("status", "NORMAL")
                })

            allocations = self.allocator.allocate(1000, assets)
            result["allocations"] = allocations

        # Portfolio Rebalance
        rebalance = self.rebalancer.rebalance(
            1000,
            brain_state["report"]
        )
        result["rebalance"] = rebalance

        # -------------------------
        # PORTFOLIO MEMORY UPDATE V7.6 (BATCH)
        # -------------------------
        self.portfolio_memory.update(rebalance)

        # -------------------------
        # 3. RISK + EXECUTION
        # -------------------------
        for item in result["allocations"]:
            approved = self.governor.approve(
                item["symbol"],
                item["allocation"],
                "NORMAL",
                1000,
                []
            )

            # Robust approval check
            if not approved: continue
            if isinstance(approved, tuple) and not approved[0]: continue
            if isinstance(approved, dict) and approved.get("decision") != "APPROVED": continue

            trade = self.execution.execute(
                {"symbol": item["symbol"], "signal": "BUY", "decision": "TRADE"},
                approved,
                size=1,
                entry=50
            )

            result["trades"].append({"symbol": item["symbol"], "trade": trade})

        # -------------------------
        # 4. FEEDBACK + LEARNING
        # -------------------------
        if result["trades"]:
            learned = []
            for item in result["trades"]:
                pnl = 100
                feedback_result = self.feedback.process_trade_result(item["symbol"], pnl)
                learned.append({"symbol": item["symbol"], "pnl": pnl, "feedback": feedback_result})

            self.feedback.learn()
            result["learning"] = {"status": "LEARNED", "results": learned}

        return result
