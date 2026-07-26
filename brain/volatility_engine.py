class VolatilityEngine:
    """
    Dynamic volatility evaluator.

    Volatility is a market metric.
    It does NOT block trading by fixed threshold.
    """

    def is_tradeable(
        self,
        volatility_percent
    ):
        return volatility_percent >= 0

    def market_state(
        self,
        volatility_percent
    ):
        if volatility_percent > 0:
            return "TRADE"

        return "NO_VOLATILITY"

    def safety_check(
        self,
        volatility_percent
    ):
        return {
            "allowed": True,
            "reason": "MARKET_DATA_VALID"
        }
