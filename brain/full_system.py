from brain.exit_strategy import ExitStrategy


class FullSystem:
    """
    MAIN TRADING BRAIN
    Production execution coordinator.

    Flow:

    MarketManager
          |
    Scanner
          v
    Signal
          v
    PositionManager
          |
    Execution
    """

    def __init__(
        self,
        alpha,
        volatility,
        trend,
        reversal,
        risk,
        leverage,
        grid,
        predictor,
        execution,
        signal_engine,
        scanner,
        portfolio_engine,
        position_manager,
        market_manager
    ):

        self.alpha = alpha
        self.volatility = volatility
        self.trend = trend
        self.reversal = reversal
        self.risk = risk
        self.leverage = leverage
        self.grid = grid
        self.predictor = predictor
        self.execution = execution
        self.signal_engine = signal_engine
        self.scanner = scanner
        self.portfolio_engine = portfolio_engine
        self.position_manager = position_manager
        self.market_manager = market_manager

        self.exit_strategy = ExitStrategy()

    def run(
        self,
        symbol,
        balance,
        stop_loss_price=None
    ):

        state = self.market_manager.get_market_state(
            symbol
        )

        if state is None:
            return "NO_MARKET_STATE"

        market = {
            "price": state.last_price,
            "volume": state.volume,
            "volatility": getattr(state, "volatility", 0) or 0,
            "change": getattr(state, "price_change_percent", 0) or 0
        }

        volatility = market.get(
            "volatility",
            0
        )

        # volatility is used by scanner/signal engine
        # no fixed volatility trade block

        market_data = {}

        for active_symbol in self.market_manager.active_symbols():

            active_state = (
                self.market_manager
                .get_market_state(active_symbol)
            )

            if active_state is None:
                continue

            market_data[active_symbol] = {
                "price": active_state.last_price,
                "volume": active_state.volume,
                "volatility": getattr(
                    active_state,
                    "volatility",
                    0
                ) or 0,
                "change": getattr(
                    active_state,
                    "price_change_percent",
                    0
                ) or 0
            }

        scan_result = self.scanner.scan(
            market_data
        )

        if scan_result == "NO_OPPORTUNITY":
            return "NO_TRADE_LOW_OPPORTUNITY"

        symbol = scan_result["symbol"]

        state = self.market_manager.get_market_state(
            symbol
        )

        signal = scan_result["signal"]

        direction = signal.get(
            "signal",
            "HOLD"
        )

        result = self.position_manager.manage(
            symbol,
            {
                "signal": direction
            },
            state.last_price,
            balance=balance,
            stop_loss_price=stop_loss_price
        )

        return {
            "mode": "MANAGED_POSITION",
            "symbol": symbol,
            "signal": direction,
            "result": result
        }
