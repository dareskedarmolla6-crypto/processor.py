import logging


logger = logging.getLogger(__name__)


class SettlementGuard:
    """
    FSE P2P Settlement Safety Gate

    Responsibilities:
    - Final safety validation
    - Combine payment and fraud checks

    Does NOT:
    - Transfer USDT
    - Execute payments
    - Create fake approvals
    """


    def __init__(
        self,
        payment_verifier,
        fraud_detector,
        merchant_scoring
    ):
        self.payment_verifier = payment_verifier
        self.fraud_detector = fraud_detector
        self.merchant_scoring = merchant_scoring


    def approve_settlement(
        self,
        payment,
        merchant
    ):

        payment_result = (
            self.payment_verifier.verify_payment(
                payment_reference=payment.get(
                    "payment_reference"
                ),
                amount=payment.get(
                    "amount"
                ),
                bank_account=payment.get(
                    "bank_account"
                )
            )
        )


        if not payment_result.get(
            "verified",
            False
        ):
            logger.warning(
                "Settlement rejected: payment verification failed"
            )
            return False



        fraud_result = (
            self.fraud_detector.analyze(
                payment
            )
        )


        if not fraud_result.get(
            "approved",
            False
        ):
            logger.warning(
                "Settlement rejected: fraud risk detected"
            )
            return False



        trusted = (
            self.merchant_scoring.is_trusted(
                merchant
            )
        )


        if not trusted:
            logger.warning(
                "Settlement rejected: merchant risk"
            )
            return False



        logger.info(
            "Settlement approved by safety gate"
        )

        return True
