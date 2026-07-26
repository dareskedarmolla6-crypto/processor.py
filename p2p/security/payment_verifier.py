import hashlib
import logging
from datetime import datetime, UTC


logger = logging.getLogger(__name__)


class PaymentVerifier:
    """
    FSE P2P Payment Verification Security Gate

    Responsibilities:
    - Validate payment proof metadata
    - Prevent duplicate payment processing
    - Track verification decisions
    - Control USDT release authorization

    Does NOT:
    - Transfer USDT
    - Trust user claims
    - Generate fake confirmations
    """

    def __init__(
        self,
        bank_verifier=None
    ):
        self.bank_verifier = bank_verifier
        self.processed_payments = set()


    def _payment_hash(
        self,
        reference,
        amount,
        account_id
    ):
        raw = (
            f"{reference}:"
            f"{amount}:"
            f"{account_id}"
        )

        return hashlib.sha256(
            raw.encode()
        ).hexdigest()


    def verify_payment(
        self,
        payment_reference,
        amount,
        bank_account
    ):
        """
        Security validation before release.

        Returns:
            {
              verified: bool,
              reason: str
            }
        """

        if not payment_reference:
            return {
                "verified": False,
                "reason": "MISSING_PAYMENT_REFERENCE"
            }


        if amount <= 0:
            return {
                "verified": False,
                "reason": "INVALID_AMOUNT"
            }


        if not bank_account.can_receive_payment():
            return {
                "verified": False,
                "reason": "BANK_ACCOUNT_NOT_AVAILABLE"
            }


        if self.bank_verifier:

            bank_result = self.bank_verifier.verify(
                reference=payment_reference,
                amount=amount,
                account_id=bank_account.account_id
            )

            if not bank_result.get(
                "verified",
                False
            ):
                return {
                    "verified": False,
                    "reason": bank_result.get(
                        "reason",
                        "BANK_VERIFICATION_FAILED"
                    )
                }


        payment_id = self._payment_hash(
            payment_reference,
            amount,
            bank_account.account_id
        )


        if payment_id in self.processed_payments:
            logger.warning(
                "Duplicate payment detected"
            )

            return {
                "verified": False,
                "reason": "DUPLICATE_PAYMENT"
            }


        self.processed_payments.add(
            payment_id
        )


        bank_account.record_transaction(
            amount
        )


        logger.info(
            f"Payment verified at {datetime.now(UTC).isoformat()}"
        )


        return {
            "verified": True,
            "reason": "PAYMENT_CONFIRMED",
            "payment_id": payment_id
        }


    def authorize_usdt_release(
        self,
        verification_result
    ):

        return (
            verification_result.get("verified")
            is True
        )
