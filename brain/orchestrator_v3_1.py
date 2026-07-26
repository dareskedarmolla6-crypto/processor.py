class OrchestratorV3_1:
    """
    FINAL CLEAN ORCHESTRATOR

    RULE:
    - volatility < 15%  → NO TRADE
    - volatility >= 15% → TRADE MODE ONLY
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
    # MAIN FLOW
    # -----------------------------
    def run(self, market, symbol, balance, drawdown):

        price = market.get("price", 0)
        change = market.get("change", 0)

        # 1. EMERGENCY STOP (FIRST PRIORITY)
        if self.risk.emergency_stop(drawdown):
            return "SYSTEM_STOP"

        # 2. VOLATILITY FILTER (STRICT 15% RULE)
        volatility = market.get("volatility", abs(change))

        if not self.volatility.is_tradeable(volatility):
            return "NO_TRADE_LOW_VOLATILITY"

        state = self.volatility.market_state(volatility)

        # 3. GRID MODE (ONLY WHEN MARKET IS WEAK SIDEWAYS INSIDE FILTERED RANGE)
        if volatility < 20:
            grid = self.grid.build_grid(price)

            return {
                "mode": "GRID",
                "state": "SIDEWAYS",
                "grid": grid
            }

        # 4. TREND MODE (STRONG MARKET ONLY)
        signal = self.predictor.predict(market)

        if isinstance(signal, dict):
            direction = signal.get("signal", "HOLD")
            confidence = signal.get("confidence", 50)
        else:
            direction, confidence = signal

        # 5. RISK + LEVERAGE
        leverage = self.leverage.calculate(confidence)
        leverage = self.risk.cap_leverage(leverage)

        approval = self.risk.check_trade(balance, balance * 0.1, [])

        if approval != "APPROVED":
            return "TRADE_BLOCKED"

        # 6. FINAL OUTPUT
        return {
            "mode": "TREND",
            "state": state,
            "signal": direction,
            "confidence": confidence,
            "leverage": leverage
        }
