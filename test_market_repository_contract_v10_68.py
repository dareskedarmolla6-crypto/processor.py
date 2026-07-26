from abc import ABC, abstractmethod
from typing import Optional

from models.symbol_state import SymbolState


class MarketStateRepository(ABC):
    """
    Market state persistence contract.

    Responsibilities:
        - Save validated market state
        - Retrieve market state
        - Check existence

    Does NOT contain:
        - Exchange communication
        - Trading logic
        - Risk logic
    """


    @abstractmethod
    def save(
        self,
        state: SymbolState
    ) -> None:
        pass


    @abstractmethod
    def get(
        self,
        symbol: str
    ) -> Optional[SymbolState]:
        pass


    @abstractmethod
    def exists(
        self,
        symbol: str
    ) -> bool:
        pass
