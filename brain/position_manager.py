from brain.smart_exit import SmartExit


class PositionManager:

    def __init__(
        self,
        execution,
        smart_exit=None,
        risk_engine=None,
        exchange_execution=None
    ):
        self.execution = execution
        self.smart_exit = smart_exit if smart_exit else SmartExit()
        self.risk_engine = risk_engine
        self.exchange_execution = exchange_execution

    def manage(self, symbol, signal, price, balance=1000, stop_loss_price=None):

        direction = signal.get("signal", "HOLD")

        positions = self.execution.positions.get(symbol, [])

        # --------------------------------------------------
        # MANAGE EXISTING POSITIONS
        # --------------------------------------------------
        for position in positions:

            if position["status"] != "OPEN":
                continue

            current_side = position["side"]

            # --------------------------------------------------
            # REVERSE POSITION LOGIC
            # LONG -> SHORT
            # SHORT -> LONG
            # --------------------------------------------------
            if (
                direction in ["SELL", "SHORT"]
                and current_side == "LONG"
            ):
                self.execution.close_by_id(
                    symbol,
                    position["id"],
                    price,
                    reason="SIGNAL_REVERSAL"
                )
                break

            if (
                direction in ["BUY", "LONG"]
                and current_side == "SHORT"
            ):
                self.execution.close_by_id(
                    symbol,
                    position["id"],
                    price,
                    reason="SIGNAL_REVERSAL"
                )
                break

            # --------------------------------------------------
            # SAME DIRECTION POSITION MONITOR
            # --------------------------------------------------
            trail = self.smart_exit.trailing_check(
                position,
                price
            )

            if isinstance(trail, dict) and trail.get("action") == "EXIT":
                return self.execution.close_by_id(
                    symbol,
                    position["id"],
                    price,
                    reason="TRAILING_STOP"
                )

            decision = self.smart_exit.decide(
                position,
                price
            )

            if decision["action"] == "PARTIAL_CLOSE":
                return self.execution.partial_close_by_id(
                    symbol,
                    position["id"],
                    decision["ratio"],
                    price
                )

            if decision["action"] == "LOCK_PROFIT":
                return self.execution.update_position_meta(
                    symbol,
                    position["id"],
                    {
                        "locked_profit": decision["profit_percent"],
                        "trailing_price": price
                    }
                )

        # --------------------------------------------------
        # HOLD
        # --------------------------------------------------
        if direction == "HOLD":
            return {
                "action": "HOLD"
            }

        # --------------------------------------------------
        # POSITION SIZE
        # --------------------------------------------------
        size = 1.0

        if self.risk_engine and stop_loss_price:
            size = self.risk_engine.calculate_position_size(
                balance,
                price,
                stop_loss_price
            )

        # --------------------------------------------------
        # OPEN NEW POSITION AFTER REVERSAL OR NEW SIGNAL
        # --------------------------------------------------
        if direction in ["BUY", "LONG"]:
            pos = self.execution.open(
                symbol,
                "LONG",
                size,
                price,
                balance
            )

            if pos == "EXCHANGE_EXECUTION_FAILED":
                return {
                    "action": "REJECTED",
                    "reason": "EXCHANGE_EXECUTION_FAILED"
                }

            return {
                "action": "OPEN",
                "side": "LONG",
                "position": pos
            }

        if direction in ["SELL", "SHORT"]:
            pos = self.execution.open(
                symbol,
                "SHORT",
                size,
                price,
                balance
            )

            if pos == "EXCHANGE_EXECUTION_FAILED":
                return {
                    "action": "REJECTED",
                    "reason": "EXCHANGE_EXECUTION_FAILED"
                }

            return {
                "action": "OPEN",
                "side": "SHORT",
                "position": pos
            }

        return {
            "action": "HOLD"
        }
