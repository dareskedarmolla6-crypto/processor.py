import logging
from datetime import datetime, UTC


logger = logging.getLogger(__name__)


class P2PMonitor:
    """
    FSE P2P Monitoring Layer

    Responsibilities:
    - Observe merchant activity
    - Track transaction events
    - Detect unusual patterns

    Does NOT:
    - Approve payments
    - Release USDT
    - Create fake reputation
    """


    def __init__(self):
        self.events = []


    def record_event(
        self,
        merchant_id,
        event_type,
        amount=0
    ):

        event = {
            "merchant_id": merchant_id,
            "event_type": event_type,
            "amount": amount,
            "timestamp": datetime.now(UTC).isoformat()
        }

        self.events.append(event)

        logger.info(
            f"P2P event recorded: {event_type}"
        )

        return event


    def merchant_activity(
        self,
        merchant_id
    ):

        return [
            event
            for event in self.events
            if event["merchant_id"] == merchant_id
        ]


    def detect_unusual_volume(
        self,
        merchant_id,
        limit
    ):

        total = sum(
            event["amount"]
            for event in self.merchant_activity(
                merchant_id
            )
        )

        if total > limit:
            return {
                "risk": True,
                "reason": "HIGH_VOLUME_ACTIVITY"
            }


        return {
            "risk": False,
            "reason": "NORMAL_ACTIVITY"
        }
