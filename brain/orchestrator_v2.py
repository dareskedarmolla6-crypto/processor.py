class OrchestratorV2:
    """
    Central brain controller.

    Responsibilities:
    - Route market data to correct strategy
    - Combine volatility + trend + confidence
    - Apply risk controls
    - Choose GRID vs TREND mode
    - Decide final action
    """

    def __init__(self, volatility_engine, trend_engine,
                 reversal_engine, risk_engine,
                 leverage_engine, grid_engine,
                 predictor):

        self.volatility = volatility_engine
        self.trend = trend_engine
        self.reversal = reversal_engine
        self.risk = risk_engine
        self.leverage = leverage_engine
        self.grid = grid_engine
        self.predictor = predictor

    # -----------------------------
    # MAIN DECISION ENGINE
    # -----------------------------
    def run(self, market, symbol, balance, drawdown):

        change = market.get("change", 0)
        price = market.get("price", 0)

        # 1. EMERGENCY STOP
        if self.risk.emergency_stop(drawdown):
            return "SYSTEM_STOP"

        # 2. VOLATILITY FILTER
        volatility = abs(change)

        if not self.volatility.is_tradeable(volatility):
            return "NO_TRADE_LOW_VOLATILITY"

        state = self.volatility.market_state(volatility)

        # -----------------------------
        # 3. SIDEWAYS MODE → GRID
        # -----------------------------
        if state == "SIDEWAYS":
            grid = self.grid.build_grid(price)
            return {
                "mode": "GRID",
                "grid": grid
            }

        # -----------------------------
        # 4. TREND MODE → PREDICTOR
        # -----------------------------
        signal, confidence = self.predictor.predict(market)

        # risk-based leverage
        leverage = self.leverage.calculate(confidence)
        leverage = self.risk.cap_leverage(leverage)

        # -----------------------------
        # 5. POSITION APPROVAL
        # -----------------------------
        if self.risk.check_trade(balance, balance * 0.1, []) != "APPROVED":
            return "TRADE_BLOCKED"

        # -----------------------------
        # 6. REVERSE FILTER (optional hook)
        # -----------------------------
        if state == "TRENDING":
            trend = self.trend.current_trend()

            if signal != trend:
                return {
                    "mode": "WAIT",
                    "reason": "trend_conflict"
                }

        # -----------------------------
        # 7. FINAL OUTPUT
        # -----------------------------
        return {
            "mode": "TREND",
            "signal": signal,
            "confidence": confidence,
            "leverage": leverage,
            "state": state
        }
