from typing import List

from market.market_feed_service import (
    MarketFeedService
)


class MarketFeedScheduler:
    """
    Production market feed scheduler.

    Responsibilities:
    - Coordinate market feed updates
    - Pass validated symbol list to feed service

    Does NOT contain:
    - Trading decisions
    - Strategy logic
    - Risk logic
    - Exchange communication
    """

    def __init__(
        self,
        feed_service: MarketFeedService
    ):
        self.feed_service = feed_service


    def run_cycle(
        self,
        symbols: List[str]
    ) -> None:
        """
        Execute one market data update cycle.
        """

        if not symbols:
            raise ValueError(
                "Symbol list cannot be empty"
            )

        self.feed_service.update_symbols(
            symbols
        )
