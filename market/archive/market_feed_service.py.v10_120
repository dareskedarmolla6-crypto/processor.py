from typing import List

from clients.binance_market_data_client import (
    BinanceMarketDataClient
)

from parsers.binance_market_data_parser import (
    BinanceMarketDataParser
)

from market.market_data_pipeline import (
    MarketDataPipeline
)


class MarketFeedService:
    """
    Production market feed coordinator.

    Responsibilities:
    - Fetch real market data
    - Parse exchange responses
    - Forward validated states to pipeline

    Does NOT contain:
    - Trading decisions
    - Strategy logic
    - Risk logic
    """

    def __init__(
        self,
        market_client: BinanceMarketDataClient,
        parser: BinanceMarketDataParser,
        pipeline: MarketDataPipeline
    ):
        self.market_client = market_client
        self.parser = parser
        self.pipeline = pipeline


    def update_symbol(
        self,
        symbol: str
    ) -> None:
        """
        Fetch and update one symbol.
        """

        response = (
            self.market_client
            .get_ticker_price(symbol)
        )

        state = (
            self.parser
            .parse_ticker_price(response)
        )

        self.pipeline.process(
            state
        )


    def update_symbols(
        self,
        symbols: List[str]
    ) -> None:
        """
        Update multiple validated symbols.
        """

        for symbol in symbols:
            self.update_symbol(symbol)
