from dataclasses import dataclass
from datetime import datetime, UTC


@dataclass
class PaymentState:
    """
    FSE P2P Payment Verification State

    Controls payment lifecycle.
    USDT release is allowed only
    after PAYMENT_VERIFIED.
    """

    payment_id: str
    merchant_id: str
    amount: float
    currency: str = "ETB"

    status: str = "CREATED"

    payer_account: str | None = None
    bank_reference: str | None = None

    verified: bool = False

    created_at: str | None = None
    verified_at: str | None = None


    ALLOWED_STATES = [
        "CREATED",
        "WAITING_PAYMENT",
        "PAYMENT_DETECTED",
        "PAYMENT_VERIFYING",
        "PAYMENT_VERIFIED",
        "USDT_RELEASE_ALLOWED",
        "COMPLETED",
        "REJECTED"
    ]


    def __post_init__(self):

        if not self.payment_id:
            raise ValueError(
                "payment_id required"
            )

        if not self.merchant_id:
            raise ValueError(
                "merchant_id required"
            )

        if self.amount <= 0:
            raise ValueError(
                "Invalid payment amount"
            )

        if self.created_at is None:
            self.created_at = (
                datetime.now(UTC)
                .isoformat()
            )


    def update_status(
        self,
        new_status: str
    ):

        if new_status not in self.ALLOWED_STATES:
            raise ValueError(
                "Invalid payment state"
            )


        self.status = new_status


        if new_status == "PAYMENT_VERIFIED":

            self.verified = True

            self.verified_at = (
                datetime.now(UTC)
                .isoformat()
            )


    def can_release_usdt(self) -> bool:
        """
        Security gate.

        Never release USDT
        before payment verification.
        """

        return (
            self.status ==
            "PAYMENT_VERIFIED"
            and
            self.verified
        )


    def reject(
        self,
        reason: str
    ):

        self.status = "REJECTED"

        self.verified = False
