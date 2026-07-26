from brain.risk_memory import RiskMemory

class RiskAdapter:
    """
    FSE Risk Adapter V8.2
    Integrated with persistent RiskMemory
    """

    def __init__(
        self,
        base_risk=0.03,
        memory=None
    ):
        self.memory = memory or RiskMemory()
        self.base_risk = base_risk
        
        # Load persistent risk state
        self.current_risk = self.memory.load(base_risk)
        self.history = []

    def apply_correction(self, correction):
        risk_change = correction.get("risk_adjustment", 0)
        
        self.current_risk += risk_change

        # Safety limits
        self.current_risk = max(
            0.01,
            min(
                self.current_risk,
                0.10
            )
        )

        # Persistent storage update
        self.memory.save(self.current_risk)

        result = {
            "previous_risk": self.base_risk,
            "current_risk": self.current_risk,
            "action": correction.get("action", "HOLD")
        }

        self.history.append(result)
        return result

    def get_risk(self):
        return round(self.current_risk, 2)

    def get_history(self):
        return self.history
