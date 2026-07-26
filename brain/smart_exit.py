class SmartExit:
    """
    SMART PROFIT MANAGEMENT ENGINE

    Features:
    - Partial profit taking
    - Profit locking
    - Trailing protection
    - Full exit decision
    """

    def __init__(self):
        self.locked_positions = {}

    # -----------------------------
    # MAIN DECISION
    # -----------------------------
    def decide(self, position, current_price):

        entry = position.get("entry", 0)
        side = position.get("side")
        size = position.get("size", 0)

        if entry <= 0 or size <= 0:
            return {
                "action": "INVALID_POSITION"
            }

        # Calculate profit %
        if side == "LONG":
            profit_percent = ((current_price - entry) / entry) * 100
        else:
            profit_percent = ((entry - current_price) / entry) * 100


        # 1. Partial profit
        if profit_percent >= 5 and profit_percent < 10:
            return {
                "action": "PARTIAL_CLOSE",
                "ratio": 0.5,
                "profit_percent": round(profit_percent, 2),
                "position_id": position.get("id")
            }


        # 2. Lock profit
        if profit_percent >= 10:

            self.locked_positions[position.get("id")] = current_price

            return {
                "action": "LOCK_PROFIT",
                "lock_price": current_price,
                "profit_percent": round(profit_percent, 2),
                "position_id": position.get("id")
            }


        # 3. Continue holding
        return {
            "action": "HOLD",
            "profit_percent": round(profit_percent, 2),
            "position_id": position.get("id")
        }


    # -----------------------------
    # TRAILING CHECK
    # -----------------------------
    def trailing_check(self, position, current_price):

        pos_id = position.get("id")

        if pos_id not in self.locked_positions:
            return "NO_LOCK"


        lock_price = self.locked_positions[pos_id]

        if position.get("side") == "LONG":

            if current_price < lock_price * 0.98:
                return {
                    "action": "EXIT",
                    "reason": "TRAILING_STOP"
                }

        else:

            if current_price > lock_price * 1.02:
                return {
                    "action": "EXIT",
                    "reason": "TRAILING_STOP"
                }


        return "PROTECTED"
