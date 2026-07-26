import logging
from collections import deque
from p2p.models.bank_account_state import BankAccountState


logger = logging.getLogger(__name__)


class AccountRotationManager:
    """
    FSE P2P Bank Account Rotation Manager

    Responsibilities:
    - Manage approved bank accounts
    - Rotate receiving accounts
    - Track account usage

    Does NOT:
    - Verify payments
    - Release USDT
    - Create fake accounts
    """

    def __init__(self):
        self.accounts = deque()

    def add_account(
        self,
        account: BankAccountState
    ):
        """
        Add a BankAccountState instance to the rotation queue.
        Validation is handled by BankAccountState initialization.
        """
        self.accounts.append(
            account
        )

    def get_next_account(self):
        """
        Rotate and return the next account that can receive payments.
        Does NOT alter transaction counts (handled by PaymentVerifier).
        """
        if not self.accounts:
            return None

        checked = len(
            self.accounts
        )

        for _ in range(checked):
            account = self.accounts.popleft()

            if account.can_receive_payment():
                self.accounts.append(
                    account
                )
                return account

            self.accounts.append(
                account
            )

        return None

    def disable_account(
        self,
        account_id: str
    ) -> bool:
        """
        Deactivate a bank account by its account_id.
        """
        for account in self.accounts:
            if account.account_id == account_id:
                account.is_active = False
                logger.warning(
                    f"Account disabled: {account_id}"
                )
                return True

        return False
