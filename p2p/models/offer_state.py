from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional
from datetime import datetime


@dataclass(slots=True)
class OfferState:
    """
    Canonical P2P offer representation.

    Every marketplace adapter converts
    its native response into this model.
    """

    provider: str

    offer_id: str

    merchant_id: str

    merchant_name: str

    price: Decimal

    available_amount: Decimal

    min_limit: Decimal

    max_limit: Decimal

    payment_methods: list[str] = field(
        default_factory=list
    )

    merchant_score: float = 0.0

    ranking_score: float = 0.0

    completion_rate: float = 0.0

    completed_orders: int = 0

    fetched_at: Optional[datetime] = None
