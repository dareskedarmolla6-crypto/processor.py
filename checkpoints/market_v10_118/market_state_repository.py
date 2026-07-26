from typing import Dict, Optional

from models.symbol_state import SymbolState


class MarketStateRepository:
    """
    Production market state persistence contract.

    Responsibilities:
    - Store validated SymbolState
    - Retrieve latest market state

    Does NOT contain:
    - Exchange communication
    - Trading logic
    - Strategy logic
    - Risk logic
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
