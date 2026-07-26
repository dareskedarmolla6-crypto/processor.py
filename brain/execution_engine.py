from datetime import datetime, UTC


class ExecutionEngine:
    """
    FSE Production Execution Engine

    Responsibilities
    ----------------
    - Open positions
    - Close positions
    - LONG / SHORT support
    - Position lifecycle management
    - Market price tracking
    - Persistence integration
    - Exchange execution integration
    """

    def __init__(
        self,
        persistence=None,
        feedback_engine=None,
        exchange_executor=None
    ):
        self.persistence = persistence
        self.feedback_engine = feedback_engine
        self.exchange_executor = exchange_executor

        self.positions = {}
        self.position_counter = 0

    def open(
        self,
        symbol,
        side,
        size,
        price,
        balance=None
    ):
        if not symbol or size <= 0 or price <= 0:
            return "INVALID_PARAMS"

        self.position_counter += 1
        if symbol not in self.positions:
            self.positions[symbol] = []

        now = datetime.now(UTC).isoformat()

        position = {
            "id": self.position_counter,
            "symbol": symbol,
            "side": side,
            "size": size,
            "entry": price,
            "status": "OPEN",
            "realized_pnl": 0.0,
            "entry_time": now,
            "last_update": now,
            "highest_price": price,
            "lowest_price": price,
            "locked_profit": 0.0,
            "trailing_price": None,
            "stop_loss": None,
            "exit": None,
            "exit_time": None,
            "close_reason": None
        }

        self.positions[symbol].append(position)

        if self.persistence:
            self.persistence.save_position(position)

        if self.exchange_executor:

            exchange_result = self.exchange_executor.execute_open(
                symbol=symbol,
                side=side,
                size=size,
                balance=balance
            )

            if not exchange_result:
                self.positions[symbol].remove(position)

                if not self.positions[symbol]:
                    del self.positions[symbol]

                return "EXCHANGE_EXECUTION_FAILED"

            position["exchange_order"] = exchange_result

        return position

    def update_market_price(
        self,
        symbol,
        pos_id,
        current_price
    ):
        if current_price <= 0:
            return "INVALID_PRICE"

        positions = self.positions.get(
            symbol,
            []
        )

        for position in positions:
            if position["id"] != pos_id:
                continue

            if position["status"] != "OPEN":
                return "NOT_OPEN"

            position["highest_price"] = max(
                position["highest_price"],
                current_price
            )

            position["lowest_price"] = min(
                position["lowest_price"],
                current_price
            )

            position["last_update"] = datetime.now(
                UTC
            ).isoformat()

            if self.persistence:
                self.persistence.update_position(
                    position
                )

            return position

        return "NOT_FOUND"

    # --------------------------------------------------
    # CLOSE POSITION
    # --------------------------------------------------
    def close_by_id(
        self,
        symbol,
        pos_id,
        price,
        reason="MANUAL"
    ):
        positions = self.positions.get(
            symbol,
            []
        )

        for position in positions:
            if position["id"] != pos_id:
                continue

            if position["status"] != "OPEN":
                return "ALREADY_CLOSED"

            pnl = (
                price - position["entry"]
            ) * position["size"]

            if position["side"] == "SHORT":
                pnl = -pnl

            now = datetime.now(
                UTC
            ).isoformat()

            position["status"] = "CLOSED"
            position["exit"] = price
            position["exit_time"] = now
            position["last_update"] = now
            position["close_reason"] = reason
            position["realized_pnl"] = pnl

            if self.persistence:
                self.persistence.update_position(
                    position
                )

            feedback = None

            if self.feedback_engine:
                feedback = self.feedback_engine.process(
                    position
                )

            return {
                "position": position,
                "feedback": feedback
            }

        return "NOT_FOUND"

    # --------------------------------------------------
    # PARTIAL CLOSE POSITION
    # --------------------------------------------------
    def partial_close_by_id(
        self,
        symbol,
        pos_id,
        ratio,
        price
    ):
        positions = self.positions.get(
            symbol,
            []
        )

        for position in positions:
            if position["id"] != pos_id:
                continue

            if position["status"] != "OPEN":
                return "NOT_OPEN"

            if ratio <= 0 or ratio >= 1:
                return "INVALID_RATIO"

            close_size = (
                position["size"]
                *
                ratio
            )

            if close_size <= 0:
                return "INVALID_SIZE"

            pnl = (
                price
                -
                position["entry"]
            ) * close_size

            if position["side"] == "SHORT":
                pnl = -pnl

            position["size"] -= close_size
            position["realized_pnl"] += pnl

            if position["size"] <= 0:
                position["size"] = 0
                position["status"] = "CLOSED"
                position["exit"] = price
                position["exit_time"] = datetime.now(
                    UTC
                ).isoformat()
                position["close_reason"] = "PARTIAL_CLOSE"

            position["last_update"] = datetime.now(
                UTC
            ).isoformat()

            if self.persistence:
                self.persistence.update_position(
                    position
                )

            return {
                "position": position,
                "closed_size": close_size,
                "realized_pnl": pnl
            }

        return "NOT_FOUND"

    # --------------------------------------------------
    # UPDATE POSITION METADATA
    # --------------------------------------------------
    def update_position_meta(
        self,
        symbol,
        pos_id,
        metadata
    ):
        positions = self.positions.get(
            symbol,
            []
        )

        for position in positions:
            if position["id"] != pos_id:
                continue

            if position["status"] != "OPEN":
                return "NOT_OPEN"

            if "locked_profit" in metadata:
                position["locked_profit"] = metadata["locked_profit"]

            if "trailing_price" in metadata:
                position["trailing_price"] = metadata["trailing_price"]

            if "highest_price" in metadata:
                position["highest_price"] = max(
                    position["highest_price"],
                    metadata["highest_price"]
                )

            if "lowest_price" in metadata:
                position["lowest_price"] = min(
                    position["lowest_price"],
                    metadata["lowest_price"]
                )

            position["last_update"] = datetime.now(
                UTC
            ).isoformat()

            if self.persistence:
                self.persistence.update_position(
                    position
                )

            return position

        return "NOT_FOUND"

    # --------------------------------------------------
    # RESTORE POSITIONS FROM PERSISTENCE
    # --------------------------------------------------
    def restore_positions(self):
        if not self.persistence:
            return

        restored_positions = (
            self.persistence.restore_positions()
        )

        for position in restored_positions:
            symbol = position["symbol"]

            if symbol not in self.positions:
                self.positions[symbol] = []

            self.positions[symbol].append(position)
            self.position_counter = max(
                self.position_counter,
                position["id"]
            )
