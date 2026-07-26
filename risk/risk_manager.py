# fse/risk/risk_manager.py
import logging

logger = logging.getLogger(__name__)

class RiskEngine:
    """Core Risk Engine: የንግድ ስራን የሚያጣራ እና የካፒታል ጥበቃ የሚያደርግ።"""
    def __init__(self, max_risk=0.02, max_exposure=0.3, max_drawdown=0.25):
        self.max_risk = float(max_risk)
        self.max_exposure = float(max_exposure)
        self.max_drawdown = float(max_drawdown)

    def validate_new_position(self, signal, balance, position_size, open_positions):
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


class RiskGovernor:
    """System-wide protection layer (Kill switch & State Control)."""
    def __init__(self, store):
        self.store = store
        self.state = {"daily_pnl": 0.0, "consecutive_losses": 0, "drawdown": 0.0}

    def update(self, pnl):
        self.state["daily_pnl"] += float(pnl)
        self.state["consecutive_losses"] = self.state["consecutive_losses"] + 1 if pnl < 0 else 0
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
    """በConfidence እና በRisk factor መሰረት የንግድ መጠን መወሰኛ።"""
    def __init__(self, max_risk=0.02):
        self.max_risk = max_risk

    def calculate(self, balance, confidence):
        risk_factor = float(confidence) / 100.0
        return round(balance * self.max_risk * risk_factor, 2)


class RiskAdjuster:
    """የገበያ ሁኔታን መሰረት አድርጎ የሌቨሬጅ አሰላል።"""
    def get_leverage(self, confidence, volatility=0.5, hedge=False):
        # FSE V11.77 Confidence Adaptive Leverage

        confidence = float(confidence)

        # ከ 40% በታች የሆነ ሲግናል የሊቨሬጅ እሴቱ 0 ይሆናል (No trade)
        if confidence < 40:
            return 0

        elif confidence < 50:
            lev = 15

        elif confidence < 60:
            lev = 25

        elif confidence < 70:
            lev = 35

        elif confidence < 80:
            lev = 45

        elif confidence < 90:
            lev = 55

        else:
            lev = 70

        # Volatility protection
        if volatility > 0.8:
            lev *= 0.7
        elif volatility > 0.6:
            lev *= 0.85

        # Hedge mode protection
        if hedge:
            lev *= 0.6

        # የድሮው የ 30x ገደብ ተወግዶ ወደ ተለዋዋጭ ማክሲመም ተቀይሯል
        return max(round(lev), 0)
