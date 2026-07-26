class HedgeEngine:
    """
    MANAGES DUAL HEDGE POSITIONS
    LONG + SHORT ON SAME SYMBOL
    """

    def __init__(self, execution):
        self.execution = execution


    def apply_hedge(self, symbol, current_price, original_side):

        hedge_side = "SHORT" if original_side == "LONG" else "LONG"

        hedge_size = 0.5

        print(
            f"HEDGE ACTIVATED: Opening {hedge_side} for {symbol} at {current_price}"
        )

        self.execution.open(
            symbol,
            hedge_side,
            hedge_size,
            current_price
        )

        return True


    def should_hedge(self, market_data):

        volatility = market_data.get(
            "volatility",
            0
        )

        return volatility > 25
