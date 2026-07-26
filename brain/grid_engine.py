class GridEngine:
    """
    Production Grid Trading Engine.

    - Builds adaptive price levels around market price.
    - Designed for low-capital crypto grid trading.
    - No exchange execution logic.
    """

    def __init__(
        self,
        grid_percent=1.5,
        levels=20
    ):
        self.grid_percent = grid_percent
        self.levels = levels

    def build_grid(
        self,
        center_price
    ):
        """
        Create buy and sell grid levels.

        Example:
        center_price = 0.0025

        Creates multiple small steps around current market price.
        """

        center_price = float(
            center_price
        )

        step = (
            center_price
            *
            self.grid_percent
            /
            100
        )

        buy_levels = []
        sell_levels = []

        for i in range(1, self.levels + 1):

            buy_price = (
                center_price
                -
                (step * i)
            )

            sell_price = (
                center_price
                +
                (step * i)
            )

            if buy_price > 0:
                buy_levels.append(
                    round(
                        buy_price,
                        8
                    )
                )

            sell_levels.append(
                round(
                    sell_price,
                    8
                )
            )

        return {
            "center": center_price,
            "grid_percent": self.grid_percent,
            "levels": self.levels,
            "buy_levels": buy_levels,
            "sell_levels": sell_levels
        }

    def get_action(
        self,
        current_price,
        grid
    ):
        current_price = float(current_price)

        tolerance = (
            current_price
            *
            0.002
        )

        for buy in grid["buy_levels"]:
            if abs(current_price - buy) <= tolerance:
                return {
                    "signal": "BUY",
                    "price": buy,
                    "source": "GRID"
                }

        for sell in grid["sell_levels"]:
            if abs(current_price - sell) <= tolerance:
                return {
                    "signal": "SELL",
                    "price": sell,
                    "source": "GRID"
                }

        return {
            "signal": "HOLD",
            "source": "GRID"
        }
