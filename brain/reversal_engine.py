class ReversalEngine:
    """
    Handles confirmed trend reversals.

    Rules:
    - Keep current position while trend is unconfirmed.
    - Close old position after confirmed reversal.
    - Open new position in the opposite direction.
    - Exit market if volatility becomes too low.
    """

    def decide(self, current_side, confirmed_trend, market_state):
        if market_state != "TRENDING":
            return "EXIT"

        if confirmed_trend == "WAIT":
            return "HOLD"

        if current_side is None:
            return f"OPEN_{confirmed_trend}"

        if current_side == confirmed_trend:
            return "HOLD"

        return f"REVERSE_TO_{confirmed_trend}"
