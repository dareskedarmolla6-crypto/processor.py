from brain.predictor import Predictor
from brain.position_engine import PositionEngine
from brain.volatility_engine import VolatilityEngine
from brain.trend_engine import TrendEngine
from brain.reversal_engine import ReversalEngine


class Orchestrator:
    """
    Main Brain Controller
    Connects all engines into one execution flow
    """

    def __init__(self):
        self.predictor = Predictor()
        self.position = PositionEngine()
        self.volatility = VolatilityEngine()
        self.trend = TrendEngine()
        self.reversal = ReversalEngine()

    def run(self, market_data, symbol, balance, drawdown):
        change = market_data.get("change", 0)

        # 1. Volatility filter
        if not self.volatility.is_tradeable(change):
            return "NO_TRADE_LOW_VOLATILITY"

        market_state = self.volatility.market_state(change)

        # 2. Trend logic
        trend_signal = self.trend.current_trend()

        # 3. AI prediction
        side, confidence = self.predictor.predict(market_data)

        # 4. Reversal decision
        reversal_action = self.reversal.decide(
            current_side=None,
            confirmed_trend=trend_signal,
            market_state=market_state
        )

        # 5. Position logic
        if reversal_action == "EXIT":
            return "EXIT_ALL"

        if reversal_action.startswith("REVERSE"):
            self.position.open_position(symbol, "LONG" if "LONG" in reversal_action else "SHORT", 1, market_data.get("price", 0))
            return reversal_action

        if confidence < 60:
            return "LOW_CONFIDENCE_HOLD"

        # default action
        self.position.open_position(symbol, side, 1, market_data.get("price", 0))
        return side
