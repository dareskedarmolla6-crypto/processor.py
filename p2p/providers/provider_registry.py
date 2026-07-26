import logging

from p2p.providers.market_provider import MarketProvider


logger = logging.getLogger(__name__)


class ProviderRegistry(MarketProvider):
    """
    Registry for production P2P market providers.

    Responsibilities:
    - Hold registered providers
    - Aggregate real offers

    Does NOT:
    - Generate fake offers
    - Execute trades
    """

    def __init__(self):
        self._providers: list[MarketProvider] = []

    def register(
        self,
        provider: MarketProvider
    ) -> None:
        self._providers.append(provider)

    def fetch_offers(
        self,
        merchant_preferences=None
    ) -> list:

        offers = []

        for provider in self._providers:
            offers.extend(
                provider.fetch_offers(
                    merchant_preferences
                )
            )

        return offers
