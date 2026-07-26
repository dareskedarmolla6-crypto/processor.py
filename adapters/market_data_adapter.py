from abc import ABC, abstractmethod
from typing import List

from models.symbol_state import SymbolState


class MarketDataAdapter(ABC):
    """
    Abstract interface for real market data providers.

    Implementations may connect to:
        - Exchange WebSocket
        - Exchange REST API
        - Other market data sources

    No market simulation belongs here.
    """

    @abstractmethod
    def connect(self) -> None:
        """
        Establish connection to market data source.
        """
        pass

    @abstractmethod
    def get_symbols(self) -> List[str]:
        """
        Return available symbols.
        """
        pass

    @abstractmethod
    def get_market_state(
        self,
        symbol: str
    ) -> SymbolState:
        """
        Return latest market state for symbol.
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Close market data connection.
        """
        pass
