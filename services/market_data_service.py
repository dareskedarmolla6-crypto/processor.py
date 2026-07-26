from typing import Dict, Any

from clients.binance_client import BinanceClient
from parsers.binance_market_data_parser import (
    BinanceMarketDataParser
)
from market.market_manager import MarketManager


class MarketDataService:
    """
    Production market data orchestration service.

    Responsibilities:
    - Fetch market data from exchange client
    - Parse validated responses
    - Push updates to MarketManager

    Does NOT contain:
    - Trading decisions
    - Strategy logic
    - Risk logic
    """

    def __init__(
        self,
        client: BinanceClient,
        parser: BinanceMarketDataParser,
        manager: MarketManager
    ):
        self.client = client
        self.parser = parser
        self.manager = manager


    def update_symbol(
        self,
        response: Dict[str, Any]
    ) -> None:
        """
        Convert exchange response
        into market state update.
        """

        state = self.parser.parse_ticker_price(
            response
        )

        self.manager.update_market_state(
            state
        )
