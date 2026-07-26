class SignalEngine:
    """
    REAL MARKET DECISION ENGINE

    Uses market-derived metrics only.

    Rules:
    - No fixed confidence values
    - No artificial trading signals
    - No volatility-only direction
    - Direction comes from real price movement

    Decision inputs:
    - price movement
    - volatility
    - volume strength
    - market momentum
    """

    def decide(
        self,
        market
    ):

        price = market.get(
            "price"
        )

        volatility = market.get(
            "volatility",
            0
        )

        volume = market.get(
            "volume",
            0
        )

        change = market.get(
            "change",
            0
        )

        if not price:
            return {
                "signal": "HOLD",
                "confidence": 0.0
            }

        #
        # Real market direction
        # comes only from price movement
        #
        momentum = change

        #
        # No valid price movement
        # means no directional decision
        #
        if momentum == 0:
            return {
                "signal": "HOLD",
                "confidence": 0.0
            }

        #
        # Market strength calculation
        # Uses real volatility and liquidity
        #
        market_pressure = (
            abs(momentum)
            *
            (1 + abs(volatility))
            *
            (1 + volume if volume else 1)
        )

        if momentum > 0:
            direction = "BUY"
        else:
            direction = "SELL"

        confidence = self._calculate_confidence(
            market_pressure
        )

        return {
            "signal": direction,
            "confidence": confidence,
            "momentum": momentum,
            "volatility": volatility,
            "volume": volume
        }

    def _calculate_confidence(
        self,
        market_pressure
    ):

        if market_pressure <= 0:
            return 0.0

        #
        # Normalize to 0–100 scale
        # Compatible with LeverageEngine
        #
        confidence = (
            market_pressure
            /
            (market_pressure + 1)
        ) * 100

        return round(confidence, 2)
