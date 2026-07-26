class AutoScanner:
    """
    Production opportunity selector.

    Flow:

    Active Market Symbols
            |
            v
    Market Intelligence
            |
            v
    Dynamic Opportunity Scoring
            |
            v
    Ranked Candidates
            |
            v
    Top Trade Candidates
    """

    TOP_CANDIDATES = 20

    def __init__(
        self,
        alpha,
        signal_engine
    ):
        self.alpha = alpha
        self.signal_engine = signal_engine

    def scan(
        self,
        market_data
    ):
        """
        Scan validated market states and rank production opportunities.
        """

        ranked = []

        for symbol, data in market_data.items():

            price = float(
                data.get(
                    "price"
                ) or 0
            )

            volume = float(
                data.get(
                    "volume"
                ) or 0
            )

            volatility = float(
                data.get(
                    "volatility"
                ) or 0
            )

            trend = float(
                data.get(
                    "trend"
                ) or 0
            )

            if price <= 0:
                continue

            alpha_score = float(
                self.alpha.score(
                    symbol,
                    data
                ) or 0
            )

            signal = self.signal_engine.decide(
                data
            )

            direction = signal.get(
                "signal",
                "HOLD"
            )

            if direction not in [
                "BUY",
                "SELL"
            ]:
                continue

            confidence = float(
                signal.get(
                    "confidence",
                    0
                )
            )

            # Production scoring: Uses real market inputs only.
            score = (
                confidence
                *
                (1 + abs(trend))
                *
                (1 + abs(volatility))
                *
                (1 + abs(alpha_score))
            )

            ranked.append(
                {
                    "symbol": symbol,
                    "price": price,
                    "volume": volume,
                    "volatility": volatility,
                    "signal": signal,
                    "confidence": confidence,
                    "score": score
                }
            )

        if not ranked:
            return "NO_OPPORTUNITY"

        ranked.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        top_candidates = ranked[
            :self.TOP_CANDIDATES
        ]

        best = top_candidates[0]

        return {
            "symbol": best["symbol"],
            "price": best["price"],
            "signal": best["signal"],
            "score": best["score"],
            "candidates": top_candidates
        }
