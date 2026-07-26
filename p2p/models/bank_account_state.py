from dataclasses import dataclass, field
from datetime import datetime, UTC


@dataclass
class BankAccountState:
    """
    FSE P2P Bank Account Management Model

    Responsibilities:
    - Approved bank account tracking
    - Account rotation support
    - Transaction health monitoring
    - Suspicious activity control

    Does NOT:
    - Execute payments
    - Release USDT
    - Verify receipts
    """

    account_id: str
    bank_name: str
    account_holder: str

    account_number: str

    status: str = "ACTIVE"

    transaction_count: int = 0
    total_volume: float = 0.0

    failed_transactions: int = 0
    suspicious_flag: bool = False

    last_used_at: str | None = None

    metadata: dict = field(
        default_factory=dict
    )


    ALLOWED_STATUS = [
        "ACTIVE",
        "PAUSED",
        "DISABLED"
    ]


    def __post_init__(self):

        if not self.account_id:
            raise ValueError(
                "account_id required"
            )

        if not self.bank_name:
            raise ValueError(
                "bank_name required"
            )

        if not self.account_number:
            raise ValueError(
                "account_number required"
            )


    def can_receive_payment(self) -> bool:
        """
        Account safety check.
        """

        return (
            self.status == "ACTIVE"
            and
            not self.suspicious_flag
        )


    def record_transaction(
        self,
        amount: float
    ):

        if amount <= 0:
            raise ValueError(
                "Invalid transaction amount"
            )

        self.transaction_count += 1
        self.total_volume += amount

        self.last_used_at = (
            datetime.now(UTC)
            .isoformat()
        )


    def mark_suspicious(self):

        self.suspicious_flag = True
        self.status = "PAUSED"


    def update_status(
        self,
        new_status: str
    ):

        if new_status not in self.ALLOWED_STATUS:
            raise ValueError(
                "Invalid account status"
            )

        self.status = new_status
