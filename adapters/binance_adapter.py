from typing import List

from adapters.market_data_adapter import MarketDataAdapter
from models.symbol_state import SymbolState


class BinanceMarketAdapter(MarketDataAdapter):
    """
    Real Binance market data adapter.

    This class will handle:
    - Binance API connection
    - Market data retrieval
    - Response normalization

    No simulated data is allowed.
    """

    def __init__(self, api_key: str = None, api_secret: str = None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.connected = False

    def connect(self) -> None:
        """
        Establish real exchange connection.

        Implementation will use Binance API client.
        """
        raise NotImplementedError(
            "Real Binance connection not implemented yet"
        )

    def get_symbols(self) -> List[str]:
        """
        Fetch real exchange symbols.
        """
        raise NotImplementedError(
            "Real symbol retrieval not implemented yet"
        )

    def get_market_state(
        self,
        symbol: str
    ) -> SymbolState:
        """
        Convert real exchange response into SymbolState.
        """
        raise NotImplementedError(
            "Real market data retrieval not implemented yet"
        )

    def close(self) -> None:
        """
        Close exchange connection.
        """
        self.connected = False
