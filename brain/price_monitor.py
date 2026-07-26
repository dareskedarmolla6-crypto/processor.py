class PriceMonitor:
    """
    FSE Live Position Monitor
    """

    def __init__(self, position_manager):
        self.manager = position_manager

    def update(
        self,
        symbol,
        price
    ):

        positions = self.manager.execution.positions.get(
            symbol,
            []
        )

        results = []

        for position in positions:

            if position["status"] != "OPEN":
                continue

            # Update live market price boundaries first
            self.manager.execution.update_market_price(
                symbol,
                position["id"],
                price
            )

            # Then evaluate exits
            result = self.manager.manage(
                symbol,
                {
                    "signal": "HOLD"
                },
                price
            )

            results.append(
                {
                    "position_id": position["id"],
                    "result": result
                }
            )

        return results
