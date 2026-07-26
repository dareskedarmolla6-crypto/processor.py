import logging

logger = logging.getLogger(__name__)


class RiskEngine:
    """
    Core Risk Engine
    FSE V11.77 Production Risk Protection
    """

    def __init__(
        self,
        max_risk=0.02,
        max_exposure=0.3,
        max_drawdown=0.25,
        max_leverage=70
    ):
        self.max_risk = float(max_risk)
        self.max_exposure = float(max_exposure)
        self.max_drawdown = float(max_drawdown)
        self.max_leverage = int(max_leverage)

        self.position_sizer = PositionSizer(max_risk=self.max_risk)

    def validate_new_position(
        self,
        signal,
        balance,
        position_size,
        open_positions
    ):
        if balance <= 0:
            return False, "INVALID_BALANCE"

        if (position_size / balance) > self.max_risk:
            return False, "RISK_TOO_HIGH"

        exposure = sum(open_positions) / balance if open_positions else 0

        if exposure > self.max_exposure:
            return False, "EXPOSURE_LIMIT"

        if signal not in ["LONG", "SHORT", "HEDGE"]:
            return False, "INVALID_SIGNAL"

        return True, "APPROVED"

    def emergency_stop(self, drawdown):
        return drawdown >= self.max_drawdown

    def cap_leverage(self, leverage, mode="NORMAL"):
        """
        FSE V11.77 Adaptive Leverage Protection

        No hidden fixed caps.
        Final maximum control is managed by max_leverage.
        """

        leverage = int(leverage)
        if leverage < 0:
            return 0
        return min(leverage, self.max_leverage)

    def calculate_position_size(
        self,
        balance,
        entry_price,
        stop_loss_price
    ):
        if (
            entry_price is None
            or stop_loss_price is None
            or entry_price <= 0
        ):
            return 0.0

        stop_distance = abs(entry_price - stop_loss_price)

        if stop_distance <= 0:
            return 0.0

        risk_amount = self.position_sizer.calculate(
            balance,
            confidence=100
        )

        return round(risk_amount / stop_distance, 8)


class RiskGovernor:
    """
    System-wide protection layer
    """

    def __init__(self, store):
        self.store = store
        self.state = {
            "daily_pnl": 0.0,
            "consecutive_losses": 0,
            "drawdown": 0.0
        }

    def update(self, pnl):
        self.state["daily_pnl"] += float(pnl)

        if pnl < 0:
            self.state["consecutive_losses"] += 1
        else:
            self.state["consecutive_losses"] = 0

        self.store.set("risk_state", self.state)

    def approve_trade(self):
        if self.store.get("system_status") in ["STOP", "EMERGENCY"]:
            return False, "SYSTEM_HALTED"

        if self.state["consecutive_losses"] >= 5:
            self._halt("CONSECUTIVE LOSSES")
            return False, "SAFE_MODE"

        return True, "OK"

    def _halt(self, reason):
        logger.warning(f"[RISK HALT] {reason}")
        self.store.set("system_status", "STOP")


class PositionSizer:
    """
    Confidence based position sizing
    """

    def __init__(self, max_risk=0.02):
        self.max_risk = max_risk

    def calculate(self, balance, confidence):
        risk_factor = float(confidence) / 100.0
        return round(
            balance * self.max_risk * risk_factor,
            2
        )


class RiskAdjuster:
    """
    Adaptive leverage controller
    FSE V11.77
    """

    def get_leverage(
        self,
        confidence,
        volatility=0.5,
        hedge=False
    ):
        confidence = float(confidence)

        # Below 40 confidence = no trade
        if confidence < 40:
            return 0

        if confidence < 50:
            leverage = 15

        elif confidence < 60:
            leverage = 25

        elif confidence < 70:
            leverage = 35

        elif confidence < 80:
            leverage = 45

        elif confidence < 90:
            leverage = 55

        else:
            leverage = 70

        # Volatility protection
        if volatility > 0.8:
            leverage *= 0.7

        elif volatility > 0.6:
            leverage *= 0.85

        # Hedge protection
        if hedge:
            leverage *= 0.6

        return leverage
