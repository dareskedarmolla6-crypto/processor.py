from typing import List

from market.market_data_coordinator import MarketDataCoordinator


class MarketDataService:
    """
    Production market data service.

    Responsibilities:
        - Coordinate multiple symbol updates
        - Delegate market data processing
        - Keep orchestration separate from market logic

    Does NOT contain:
        - Exchange communication
        - Symbol generation
        - Fake market data
        - Trading logic
    """

    def __init__(
        self,
        coordinator: MarketDataCoordinator
    ):
        self._coordinator = coordinator


    def update(
        self,
        symbols: List[str]
    ) -> None:
        """
        Update market data for provided symbols.
        """

        if not symbols:
            raise ValueError(
                "Symbols cannot be empty"
            )

        for symbol in symbols:

            if not symbol:
                raise ValueError(
                    "Symbol cannot be empty"
                )

            self._coordinator.update_symbol(
                symbol
            )
