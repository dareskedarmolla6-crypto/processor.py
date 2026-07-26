import logging
from p2p.providers.market_provider import MarketProvider
from p2p.models.offer_state import OfferState


logger = logging.getLogger(__name__)


class OfferRouter:
    """
    FSE P2P Market Offer Router

    Responsibilities:
    - Collect available offers
    - Rank offers
    - Select suitable offer

    Does NOT:
    - Execute payment
    - Release USDT
    - Create fake offers
    """

    def __init__(
        self,
        provider: MarketProvider,
        min_score=0
    ):
        self.provider = provider
        self.min_score = min_score

    def rank_offers(
        self,
        offers: list
    ) -> list:
        """
        Rank real offers received
        from external P2P providers.
        """
        if not offers:
            return []

        valid_offers = []

        for offer in offers:

            if not self._validate_offer(offer):
                continue

            score = self._calculate_score(
                offer
            )

            offer.ranking_score = score

            valid_offers.append(
                offer
            )

        return sorted(
            valid_offers,
            key=lambda x: x.ranking_score,
            reverse=True
        )

    def select_best_offer(
        self,
        offers: list
    ):
        """
        Return highest ranked offer.
        """

        ranked = self.rank_offers(
            offers
        )

        if not ranked:
            return None
        return ranked[0]

    def _validate_offer(
        self,
        offer: OfferState
    ) -> bool:
        """
        Validate normalized offer.
        """

        if offer.price <= 0:
            return False

        if offer.available_amount <= 0:
            return False

        if not offer.merchant_id:
            return False

        if not offer.offer_id:
            return False

        return True

    def _calculate_score(
        self,
        offer: OfferState
    ) -> float:

        score = 0.0

        # Price weight
        score += 50

        # Liquidity
        if offer.available_amount > 0:
            score += 25

        # Merchant reputation
        score += min(
            offer.merchant_score,
            25
        )

        return score

    def find_best_offer(
        self,
        merchant_preferences=None
    ):
        """
        Fetch real offers from provider,
        then rank and select the best one.
        """

        offers = self.provider.fetch_offers(
            merchant_preferences
        )

        return self.select_best_offer(
            offers
        )
