import logging
from abc import ABC, abstractmethod


logger = logging.getLogger(__name__)


class BankVerificationProvider(ABC):
    """
    External bank verification interface.

    Implementations may connect to:
    - Bank API
    - Banking webhook
    - SMS parser service

    Does NOT:
    - Create fake confirmations
    - Assume payment success
    """

    @abstractmethod
    def verify_transaction(
        self,
        reference: str,
        amount: float,
        account_id: str
    ) -> dict:
        raise NotImplementedError



class BankVerifier:
    """
    FSE P2P Bank Verification Security Gate

    Responsibilities:
    - Validate external bank confirmation
    - Match reference
    - Match amount
    - Match receiving account

    Does NOT:
    - Transfer funds
    - Release USDT
    - Generate confirmations
    """

    def __init__(
        self,
        provider: BankVerificationProvider
    ):
        self.provider = provider


    def verify(
        self,
        reference: str,
        amount: float,
        account_id: str
    ) -> dict:
        """
        Verify real bank transaction.

        Returns:
            {
                verified: bool,
                reason: str
            }
        """

        if not reference:
            return {
                "verified": False,
                "reason": "MISSING_REFERENCE"
            }


        if amount <= 0:
            return {
                "verified": False,
                "reason": "INVALID_AMOUNT"
            }


        result = self.provider.verify_transaction(
            reference,
            amount,
            account_id
        )


        if not result.get(
            "verified",
            False
        ):
            logger.warning(
                "Bank verification failed"
            )

            return {
                "verified": False,
                "reason": result.get(
                    "reason",
                    "BANK_REJECTED"
                )
            }


        logger.info(
            "Bank transaction verified"
        )


        return {
            "verified": True,
            "reason": "BANK_CONFIRMED"
        }
