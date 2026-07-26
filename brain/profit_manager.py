class ProfitManager:
    """
    Profit management engine.

    Features
    --------
    - Profit locking
    - Partial take profit
    - Trailing stop calculation
    - Alpha coin support
    """

    def __init__(
        self,
        lock_percent=50,
        partial_levels=(5, 10, 15),
        partial_size=0.25,
        trailing_stop=3
    ):
        self.lock_percent = lock_percent
        self.partial_levels = list(partial_levels)
        self.partial_size = partial_size
        self.trailing_stop = trailing_stop

    def profit_percent(self, entry, current, side):
        if side == "LONG":
            return ((current - entry) / entry) * 100

        if side == "SHORT":
            return ((entry - current) / entry) * 100

        return 0.0

    def locked_profit(self, profit):
        if profit <= 0:
            return 0.0

        return round(profit * self.lock_percent / 100, 2)

    def partial_signal(self, profit):
        for level in sorted(self.partial_levels):
            if profit >= level:
                return {
                    "action": "PARTIAL_CLOSE",
                    "close_size": self.partial_size,
                    "level": level
                }

        return None

    def trailing_price(self, highest_price):
        return highest_price * (
            1 - self.trailing_stop / 100
        )
