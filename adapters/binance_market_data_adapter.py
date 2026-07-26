from clients.binance_market_data_client import BinanceMarketDataClient
from parsers.binance_market_data_parser import BinanceMarketDataParser
from models.symbol_state import SymbolState


class BinanceMarketDataAdapter:
    """
    Production Binance market data adapter.

    Responsibilities:
    - Retrieve raw Binance market data
    - Convert exchange response into SymbolState

    Does NOT contain:
    - Trading logic
    - Strategy logic
    - Risk logic
    """


    def __init__(
        self,
        client: BinanceMarketDataClient,
        parser: BinanceMarketDataParser
    ):
        self._client = client
        self._parser = parser


    def from_24h(
        self,
        symbol: str
    ) -> SymbolState:
        """
        Retrieve Binance 24h ticker
        and convert into domain state.
        """

        response = self._client.get_ticker_24h(
            symbol
        )

        return self._parser.parse_ticker_price(
            response
        )
