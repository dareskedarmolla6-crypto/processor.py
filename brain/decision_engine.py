class DecisionEngine:
    """
    Final decision layer.

    Combines:
    - Predictor
    - Volatility
    - Trend confirmation

    Returns one of:
    BUY
    SELL
    HOLD
    """

    def decide(self, prediction, market_state, trend):

        if market_state != "TRENDING":
            return "HOLD"

        if trend == "WAIT":
            return "HOLD"

        if prediction == "BUY" and trend == "LONG":
            return "BUY"

        if prediction == "SELL" and trend == "SHORT":
            return "SELL"

        return "HOLD"
