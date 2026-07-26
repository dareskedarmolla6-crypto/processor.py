from typing import Dict, Optional

from repositories.market_repository import MarketRepository
from models.symbol_state import SymbolState


class InMemoryMarketRepository(MarketRepository):
    """
    In-memory implementation of the market repository.

    Used for:
    - Runtime state
    - Unit tests

    Does NOT persist data across restarts.
    """

    def __init__(self):
        self._states: Dict[str, SymbolState] = {}

    def save(
        self,
        state: SymbolState
    ) -> None:
        self._states[state.symbol] = state

    def get(
        self,
        symbol: str
    ) -> Optional[SymbolState]:
        return self._states.get(symbol)

    def exists(
        self,
        symbol: str
    ) -> bool:
        return symbol in self._states
