from clients.binance_market_data_client import BinanceMarketDataClient
from market.binance_market_adapter import BinanceMarketAdapter


class RealMarketFeedAdapter:
    """
    Production bridge between
    Binance client and MarketFeed.

    Responsibilities:
    - Fetch real Binance data
    - Convert to SymbolState
    - Return unified market snapshot
    """


    def __init__(
        self,
        client: BinanceMarketDataClient,
        symbols: list
    ):

        self.client = client
        self.converter = BinanceMarketAdapter()
        self.symbols = symbols


    def fetch(self):

        snapshot = []


        for symbol in self.symbols:

            raw = self.client.get_ticker_price(
                symbol
            )


            state = self.converter.from_ticker(
                raw
            )


            snapshot.append(
                {
                    "symbol": state.symbol,
                    "exchange": state.exchange,
                    "price": state.last_price
                }
            )


        if not snapshot:
            raise RuntimeError(
                "Empty market snapshot"
            )


        return snapshot
