from brain.self_optimizer import SelfOptimizer


class AdaptiveBrain:
    """
    FSE Adaptive Brain V9.1

    Features
    --------
    - Performance Memory
    - Self Optimizer
    - Portfolio Feedback Injection
    - Market Regime Awareness
    """

    def __init__(
        self,
        performance_memory,
        portfolio_feedback=None,
        market_regime=None,
        min_confidence=0.75
    ):
        self.memory = performance_memory
        self.optimizer = SelfOptimizer(performance_memory)

        self.portfolio_feedback = portfolio_feedback
        self.market_regime = market_regime

        self.min_confidence = min_confidence
        self.risk_level = 0.03

        self.feedback_adjustments = {}

    # ---------------------------------
    # Portfolio Feedback
    # ---------------------------------

    def inject_feedback(self, feedback):

        self.feedback_adjustments = {}

        for symbol, data in feedback.items():
            self.feedback_adjustments[symbol] = data.get(
                "adjustment",
                0
            )

        return self.feedback_adjustments

    # ---------------------------------
    # Optimizer
    # ---------------------------------

    def optimize(self):

        state = self.optimizer.optimize()

        self.min_confidence = state["confidence_threshold"]
        self.risk_level = state["risk_level"]

        return state

    # ---------------------------------
    # Evaluate
    # ---------------------------------

    def evaluate(self, signal):

        self.optimize()

        symbol = signal["symbol"]

        confidence = self.memory.adjust_confidence(
            symbol,
            signal["confidence"]
        )

        confidence += self.feedback_adjustments.get(
            symbol,
            0
        )

        # -----------------------------
        # Market Regime Integration
        # -----------------------------
        regime_info = None

        if self.market_regime:

            regime_info = self.market_regime.get_current()

            confidence += regime_info.get(
                "confidence_bonus",
                0
            )

            self.risk_level *= regime_info.get(
                "risk_multiplier",
                1.0
            )

        confidence = max(
            0,
            min(
                confidence,
                1
            )
        )

        decision = (
            "TRADE"
            if confidence >= self.min_confidence
            else "SKIP"
        )

        return {
            "symbol": symbol,
            "signal": signal["signal"],
            "confidence": round(confidence, 2),
            "decision": decision,
            "brain_threshold": round(
                self.min_confidence,
                2
            ),
            "risk_level": round(
                self.risk_level,
                4
            ),
            "market_regime": (
                regime_info["regime"]
                if regime_info
                else "UNKNOWN"
            )
        }
