class OrchestratorV3:
    """
    FINAL brain controller.

    Fixes:
    - Correct volatility interpretation
    - Proper GRID vs TREND routing
    - Risk + leverage integration
    - Clean decision flow
    """

    def __init__(self,
                 volatility_engine,
                 trend_engine,
                 reversal_engine,
                 risk_engine,
                 leverage_engine,
                 grid_engine,
                 predictor):

        self.volatility = volatility_engine
        self.trend = trend_engine
        self.reversal = reversal_engine
        self.risk = risk_engine
        self.leverage = leverage_engine
        self.grid = grid_engine
        self.predictor = predictor

    # -----------------------------
    # MAIN BRAIN
    # -----------------------------
    def run(self, market, symbol, balance, drawdown):

        change = market.get("change", 0)
        price = market.get("price", 0)

        # 1. EMERGENCY STOP
        if self.risk.emergency_stop(drawdown):
            return "SYSTEM_STOP"

        # 2. VOLATILITY CHECK (correct logic)
        volatility = abs(change)

        if not self.volatility.is_tradeable(volatility):
            return "NO_TRADE_LOW_VOLATILITY"

        state = self.volatility.market_state(volatility)

        # -----------------------------
        # 3. GRID MODE (SIDEWAYS)
        # -----------------------------
        if state == "SIDEWAYS":
            grid = self.grid.build_grid(price)

            return {
                "mode": "GRID",
                "state": state,
                "grid": grid
            }

        # -----------------------------
        # 4. TREND MODE (ACTIVE MARKET)
        # -----------------------------
        signal = self.predictor.predict(market)

        # ensure compatibility (dict or tuple safe handling)
        if isinstance(signal, dict):
            direction = signal.get("signal", "HOLD")
            confidence = signal.get("confidence", 50)
        else:
            direction, confidence = signal

        # 5. RISK CONTROL
        leverage = self.leverage.calculate(confidence)
        leverage = self.risk.cap_leverage(leverage)

        # 6. TRADE APPROVAL
        approval = self.risk.check_trade(balance, balance * 0.1, [])

        if approval != "APPROVED":
            return "TRADE_BLOCKED"

        # -----------------------------
        # 7. FINAL DECISION
        # -----------------------------
        return {
            "mode": "TREND",
            "state": state,
            "signal": direction,
            "confidence": confidence,
            "leverage": leverage
        }
