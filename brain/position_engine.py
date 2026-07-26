class PositionEngine:
    """
    Allows LONG + SHORT simultaneously per coin
    Supports grid and alpha volatility mode
    """

    def __init__(self):
        self.positions = {}

    def open_position(self, symbol, side, size, price):
        if symbol not in self.positions:
            self.positions[symbol] = {
                "LONG": [],
                "SHORT": []
            }

        self.positions[symbol][side].append({
            "size": size,
            "entry": price
        })

    def close_partial(self, symbol, side, size):
        """
        Partial take profit.
        Removes position size gradually instead of closing everything.
        """

        if symbol not in self.positions:
            return

        remaining = size

        for pos in self.positions[symbol][side]:
            if remaining <= 0:
                break

            if pos["size"] <= remaining:
                remaining -= pos["size"]
                pos["size"] = 0
            else:
                pos["size"] -= remaining
                remaining = 0

        self.positions[symbol][side] = [
            p for p in self.positions[symbol][side]
            if p["size"] > 0
        ]

    def get_exposure(self, symbol):
        pos = self.positions.get(
            symbol,
            {
                "LONG": [],
                "SHORT": []
            }
        )

        long_size = sum(p["size"] for p in pos["LONG"])
        short_size = sum(p["size"] for p in pos["SHORT"])

        return {
            "LONG": long_size,
            "SHORT": short_size,
            "NET": long_size - short_size
        }
