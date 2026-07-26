class ExitStrategy:
    """
    EXIT MANAGEMENT ENGINE

    Responsibilities:
    - Partial profit taking
    - Profit lock decision
    - Stop protection logic
    - Position exit signals
    """

    def __init__(self):
        self.partial_targets = [
            0.30,
            0.50,
            0.70
        ]

        self.profit_lock_threshold = 0.05


    # -----------------------------
    # CHECK PROFIT LEVEL
    # -----------------------------
    def check_profit(self, position, current_price):

        entry = position.get("entry", 0)
        size = position.get("size", 0)
        side = position.get("side", "LONG")

        if entry <= 0 or size <= 0:
            return "INVALID_POSITION"


        change = (current_price - entry) / entry


        if side == "SHORT":
            change = -change


        return {
            "profit_percent": change * 100,
            "side": side,
            "position_id": position.get("id")
        }


    # -----------------------------
    # EXIT DECISION
    # -----------------------------
    def decide(self, position, current_price):

        result = self.check_profit(position, current_price)

        if isinstance(result, str):
            return result


        profit = result["profit_percent"] / 100


        # Profit Lock
        if profit >= self.profit_lock_threshold:
            return {
                "action": "LOCK_PROFIT",
                "position_id": result["position_id"],
                "profit": result["profit_percent"]
            }


        # Partial Profit
        if profit > 0:
            for target in self.partial_targets:
                if profit >= target:
                    return {
                        "action": "PARTIAL_CLOSE",
                        "ratio": target,
                        "position_id": result["position_id"],
                        "profit": result["profit_percent"]
                    }


        # No action
        return {
            "action": "HOLD",
            "position_id": result["position_id"],
            "profit": result["profit_percent"]
        }
