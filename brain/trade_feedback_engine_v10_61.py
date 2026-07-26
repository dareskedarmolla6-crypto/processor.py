from datetime import datetime, UTC


class TradeFeedbackEngineV10_61:
    """
    Production Trade Feedback Engine

    Responsibilities
    ----------------
    - Validate closed positions
    - Generate immutable feedback
    - Compute trade outcome
    - Provide learning-ready records
    """

    REQUIRED_FIELDS = (
        "id",
        "symbol",
        "side",
        "entry",
        "exit",
        "status",
        "realized_pnl",
        "exit_time",
    )

    def process(self, position: dict) -> dict:

        if not isinstance(position, dict):
            raise TypeError(
                "Position must be a dictionary."
            )

        for field in self.REQUIRED_FIELDS:
            if field not in position:
                raise KeyError(
                    f"Missing field: {field}"
                )

        if position["status"] != "CLOSED":
            raise ValueError(
                "Only CLOSED positions generate feedback."
            )

        pnl = float(position["realized_pnl"])

        if pnl > 0:
            outcome = "WIN"
        elif pnl < 0:
            outcome = "LOSS"
        else:
            outcome = "BREAKEVEN"

        return {
            "position_id": position["id"],
            "symbol": position["symbol"],
            "side": position["side"],
            "entry_price": position["entry"],
            "exit_price": position["exit"],
            "realized_pnl": pnl,
            "outcome": outcome,
            "closed_at": position["exit_time"],
            "processed_at": datetime.now(
                UTC
            ).isoformat(),
        }
