import logging
from abc import ABC, abstractmethod
from p2p.models.offer_state import OfferState


logger = logging.getLogger(__name__)


class MarketProvider(ABC):
    """
    FSE P2P Market Provider Interface

    Responsibilities:
    - Connect to external P2P marketplaces
    - Fetch real offers
    - Return normalized offer list

    Does NOT:
    - Generate fake offers
    - Rank offers
    - Execute trades
    - Release USDT
    """

    @abstractmethod
    def fetch_offers(
        self,
        merchant_preferences=None
    ) -> list[OfferState]:
        """
        Return normalized offers
        from external marketplaces.

        Returns:
            List[OfferState]
        """
        raise NotImplementedError
