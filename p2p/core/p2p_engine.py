import logging
from datetime import datetime, UTC

logger = logging.getLogger(__name__)


class P2PEngine:
    """
    FSE P2P Core Engine

    Responsibilities:
    - Coordinate P2P workflow
    - Select offers
    - Select bank accounts
    - Validate settlement path

    Does NOT:
    - Hold funds
    - Release USDT directly
    - Fake payment confirmations
    """

    def __init__(
        self,
        offer_router,
        account_rotation,
        settlement_guard
    ):
        self.offer_router = offer_router
        self.account_rotation = account_rotation
        self.settlement_guard = settlement_guard

        self.orders = {}

    def create_sell_order(
        self,
        amount,
        merchant_preferences=None
    ):
        """
        Create USDT sell workflow.
        Final bot operation:
        SELL ONLY
        """

        if amount <= 0:
            raise ValueError(
                "Invalid amount"
            )

        offer = self.offer_router.find_best_offer(
            merchant_preferences
        )

        if not offer:
            logger.warning(
                "No suitable offer found"
            )
            return None

        bank_account = (
            self.account_rotation.get_next_account()
        )

        if not bank_account:
            logger.warning(
                "No active bank account available"
            )
            return None

        order_id = (
            f"P2P_{datetime.now(UTC).timestamp()}"
        )

        self.orders[order_id] = {
            "order_id": order_id,
            "amount": amount,
            "offer": offer,
            "bank_account": bank_account,
            "status": "WAITING_PAYMENT",
            "created_at": datetime.now(UTC).isoformat()
        }

        logger.info(
            f"P2P sell order created: {order_id}"
        )

        return self.orders[order_id]

    def confirm_payment_and_settle(
        self,
        order_id,
        payment,
        merchant
    ):

        order = self.orders.get(
            order_id
        )

        if not order:
            return None

        approved = (
            self.settlement_guard.approve_settlement(
                payment,
                merchant
            )
        )

        if not approved:
            order["status"] = "REJECTED"

            return {
                "status": "REJECTED",
                "reason": "Settlement safety failed"
            }

        order["status"] = "USDT_RELEASE_ALLOWED"

        return {
            "status": "USDT_RELEASE_ALLOWED",
            "order_id": order_id
        }
