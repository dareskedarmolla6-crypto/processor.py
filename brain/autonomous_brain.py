from brain.adaptive_brain import AdaptiveBrain
from brain.self_optimizer import SelfOptimizer

class AutonomousBrain:
    """
    FSE Autonomous Brain Controller
    """

    def __init__(
        self,
        performance_memory
    ):
        self.memory = performance_memory
        self.adaptive_brain = AdaptiveBrain(
            performance_memory
        )
        self.optimizer = SelfOptimizer(
            performance_memory
        )

    # -------------------------
    # Process Market Signals
    # -------------------------
    def process(
        self,
        signals
    ):
        decisions = []

        for signal in signals:
            # signal dict ውስጥ price ካለ ማለፍ
            result = self.adaptive_brain.evaluate(
                signal
            )
            
            # price መረጃውን እዚህ እናረጋግጣለን
            decisions.append({
                "symbol": result["symbol"],
                "price": signal.get("price", 0),  # እዚህ price ተጨምሯል
                "signal": result["signal"],
                "confidence": result["confidence"],
                "decision": result["decision"]
            })

        return decisions

    # -------------------------
    # Learning Update
    # -------------------------
    def learn(self):
        optimization = self.optimizer.optimize()
        self.adaptive_brain.min_confidence = (
            optimization["confidence_threshold"]
        )
        return optimization

    # -------------------------
    # Full Brain Cycle
    # -------------------------
    def run_cycle(
        self,
        signals
    ):
        decisions = self.process(
            signals
        )
        learning = self.learn()
        return {
            "decisions": decisions,
            "learning": learning
        }
