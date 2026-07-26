from abc import ABC, abstractmethod
from typing import Optional

from models.symbol_state import SymbolState


class MarketRepository(ABC):
    """
    Storage contract for market states.
    """

    @abstractmethod
    def save(
        self,
        state: SymbolState
    ) -> None:
        ...

    @abstractmethod
    def get(
        self,
        symbol: str
    ) -> Optional[SymbolState]:
        ...

    @abstractmethod
    def exists(
        self,
        symbol: str
    ) -> bool:
        ...
