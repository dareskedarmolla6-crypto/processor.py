from brain.risk_adapter import RiskAdapter
from brain.self_correction import SelfCorrection
from brain.autonomous_memory import AutonomousMemory


class AutonomousControllerV8_8:
    """
    FSE Autonomous Controller V8.8.1
    Integrated with Shared RiskAdapter, Unified Memory, and Cycle History
    """

    def __init__(
        self,
        brain,
        governor,
        execution
    ):
        self.brain = brain
        self.governor = governor
        self.execution = execution

        # V8.8.1: Instance sharing with governor
        self.risk_adapter = governor.risk_adapter or RiskAdapter()
        self.self_correction = SelfCorrection()
        self.memory = AutonomousMemory()

        self.cycle = 0

    def run_cycle(self, signals):
        self.cycle += 1
        result = {
            "cycle": self.cycle,
            "decisions": [],
            "trades": [],
            "risk": None
        }

        # -----------------
        # BRAIN
        # -----------------
        decisions = [self.brain.evaluate(x) for x in signals]
        result["decisions"] = decisions

        # -----------------
        # EXECUTION
        # -----------------
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

            if approved.get("decision") != "APPROVED":
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

            result["trades"].append({
                "symbol": item["symbol"],
                "trade": trade
            })

        # -----------------
        # LEARNING
        # -----------------
        if result["trades"]:
            correction = self.self_correction.analyze(
                [{"symbol": x["symbol"], "pnl": 100} for x in result["trades"]]
            )

            risk_result = self.risk_adapter.apply_correction(correction)
            result["risk"] = risk_result

            # -----------------
            # MEMORY SAVE
            # -----------------
            self.memory.update_risk(risk_result["current_risk"])
            
            # V8.8.1: Record full cycle history
            self.memory.record_cycle(result)

        return result
