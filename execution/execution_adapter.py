class ExecutionAdapter:

    def __init__(self, coordinator):
        self.coordinator = coordinator

    def execute_open(
        self,
        symbol,
        side,
        size,
        balance=None
    ):

        exchange_side = (
            "BUY"
            if side == "LONG"
            else "SELL"
        )

        signal = {
            "symbol": symbol,
            "side": side,
            "exchange_side": exchange_side,
            "qty": size,
            "balance": balance,
            "strategy_id": "POSITION_MANAGER",
            "leverage": 0
        }

        return self.coordinator.execute_signal(signal)
