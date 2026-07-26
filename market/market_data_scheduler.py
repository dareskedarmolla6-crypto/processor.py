from typing import List

from market.market_data_service import MarketDataService


class MarketDataScheduler:
    """
    Production market data scheduler.

    Responsibilities:
        - Trigger market data updates
        - Forward validated symbol collections
        - Keep scheduling separate from data processing

    Does NOT contain:
        - Exchange communication
        - Market data generation
        - Trading logic
        - Symbol discovery
    """

    def __init__(
        self,
        service: MarketDataService
    ):
        self._service = service


    def run_once(
        self,
        symbols: List[str]
    ) -> None:
        """
        Execute one market data update cycle.
        """

        if not symbols:
            raise ValueError(
                "Symbols cannot be empty"
            )

        self._service.update(
            symbols
        )
