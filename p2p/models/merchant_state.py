from dataclasses import dataclass
from datetime import datetime, UTC


@dataclass
class MerchantState:
    """
    FSE P2P Merchant Intelligence State

    Stores verified merchant history.
    """

    merchant_id: str

    total_trades: int = 0
    completed_trades: int = 0
    failed_trades: int = 0
    dispute_count: int = 0

    average_payment_time: float = 0.0

    trust_score: float = 0.0

    status: str = "UNKNOWN"

    last_trade_time: str | None = None


    def __post_init__(self):

        if not self.merchant_id:
            raise ValueError(
                "merchant_id required"
            )

        if self.total_trades < 0:
            raise ValueError(
                "Invalid trade count"
            )

        if self.completed_trades < 0:
            raise ValueError(
                "Invalid completed trades"
            )


    def update_trust_score(self):

        if self.total_trades == 0:
            self.trust_score = 0
            self.status = "NEW"
            return


        completion_rate = (
            self.completed_trades /
            self.total_trades
        )


        dispute_penalty = (
            self.dispute_count /
            self.total_trades
        )


        score = (
            completion_rate * 100
        ) - (
            dispute_penalty * 50
        )


        self.trust_score = max(
            0,
            min(score, 100)
        )


        if self.trust_score >= 90:
            self.status = "TRUSTED"

        elif self.trust_score >= 70:
            self.status = "NORMAL"

        else:
            self.status = "RISK"


    def record_trade(
        self,
        success: bool,
        dispute: bool = False
    ):

        self.total_trades += 1

        if success:
            self.completed_trades += 1
        else:
            self.failed_trades += 1


        if dispute:
            self.dispute_count += 1


        self.last_trade_time = (
            datetime.now(UTC)
            .isoformat()
        )


        self.update_trust_score()
