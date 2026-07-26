from threading import RLock
from typing import Dict, List, Optional

from models.symbol_state import SymbolState


class SymbolRegistry:
    """
    Production-grade registry for market symbols.

    Responsibilities:
        - Register symbols
        - Update symbol states
        - Retrieve current state
        - Remove symbols
        - Return registry snapshots

    Thread-safe for concurrent market updates.
    """

    def __init__(self):
        self._symbols: Dict[str, SymbolState] = {}
        self._lock = RLock()

    def register(self, state: SymbolState) -> None:
        with self._lock:
            self._symbols[state.symbol] = state

    def update(self, state: SymbolState) -> None:
        with self._lock:
            self._symbols[state.symbol] = state

    def get(self, symbol: str) -> Optional[SymbolState]:
        with self._lock:
            return self._symbols.get(symbol)

    def remove(self, symbol: str) -> None:
        with self._lock:
            self._symbols.pop(symbol, None)

    def exists(self, symbol: str) -> bool:
        with self._lock:
            return symbol in self._symbols

    def symbols(self) -> List[str]:
        with self._lock:
            return list(self._symbols.keys())

    def snapshot(self) -> Dict[str, SymbolState]:
        with self._lock:
            return dict(self._symbols)

    def __len__(self) -> int:
        with self._lock:
            return len(self._symbols)
