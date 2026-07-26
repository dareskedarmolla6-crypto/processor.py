import logging

logger = logging.getLogger(__name__)


class P2PService:
    """
    FSE P2P Integration Service

    Coordinates:
    - Offer evaluation
    - Merchant scoring
    - Risk checks
    - Payment verification flow

    Does NOT:
    - Execute payments
    - Release USDT
    - Bypass security checks
    """

    def __init__(
        self,
        offer_router=None,
        merchant_scoring=None,
        risk_controller=None,
        payment_verifier=None,
        fraud_detector=None,
        settlement_guard=None
    ):

        self.offer_router = offer_router
        self.merchant_scoring = merchant_scoring
        self.risk_controller = risk_controller
        self.payment_verifier = payment_verifier
        self.fraud_detector = fraud_detector
        self.settlement_guard = settlement_guard

    def evaluate_offer(
        self,
        offer
    ):
        if not offer:
            return {
                "approved": False,
                "reason": "EMPTY_OFFER"
            }

        if self.merchant_scoring:

            merchant_data = getattr(
                offer,
                "merchant",
                offer
            )

            score = self.merchant_scoring.calculate_score(
                merchant_data
            )

            if score < 70:
                return {
                    "approved": False,
                    "reason": "MERCHANT_SCORE_FAILED"
                }

        if self.risk_controller:

            amount = getattr(
                offer,
                "available_amount",
                0
            )

            price = getattr(
                offer,
                "price",
                0
            )

            risk_result = (
                self.risk_controller.validate_sell(
                    amount=amount,
                    price=price,
                    current_balance=amount
                )
            )

            approved, reason = risk_result

            if not approved:
                return {
                    "approved": False,
                    "reason": reason
                }

        logger.info(
            "P2P offer evaluation completed"
        )

        return {
            "approved": True,
            "offer": offer
        }

    def verify_payment(
        self,
        payment,
        merchant
    ):
        """
        Production payment verification workflow.

        Security decision is delegated to
        SettlementGuard.

        Does NOT release USDT.
        """

        if not self.settlement_guard:
            return {
                "verified": False,
                "reason": "SETTLEMENT_GUARD_UNAVAILABLE"
            }

        approved = self.settlement_guard.approve_settlement(
            payment,
            merchant
        )

        if not approved:
            return {
                "verified": False,
                "reason": "SETTLEMENT_REJECTED"
            }

        return {
            "verified": True,
            "reason": "PAYMENT_VERIFIED"
        }
