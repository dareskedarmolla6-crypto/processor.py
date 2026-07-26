from typing import Optional, List
from models.symbol_state import SymbolState
from market.symbol_registry import SymbolRegistry
from repositories.market_repository import MarketRepository  # የተስተካከለ Import


class MarketManager:
    """
    Production market state coordinator.

    Responsibilities:
        - Manage active market symbols
        - Coordinate validated market state updates
        - Provide market state access layer

    Exchange connectivity remains outside this class.
    Real exchange adapters push validated state here.
    """

    def __init__(
        self,
        repository: Optional[MarketRepository] = None  # የተስተካከለ Type Hint
    ):
        self._registry = SymbolRegistry()
        self._active_symbols = set()

        # Dependency Injection ከጠንካራ የፕሮዳክሽን ታይፒንግ ጋር
        self._repository = repository

    def activate_symbol(
        self,
        state: SymbolState
    ) -> None:
        """
        Activate validated market symbol.
        """

        if not state.symbol:
            raise ValueError(
                "Symbol cannot be empty"
            )

        self._registry.register(state)
        self._active_symbols.add(
            state.symbol
        )

        # Persistence integration layer
        if self._repository:
            self._repository.save(state)

    def deactivate_symbol(
        self,
        symbol: str
    ) -> None:
        """
        Remove symbol from active tracking.
        """

        self._active_symbols.discard(symbol)
        self._registry.remove(symbol)

    def update_market_state(
        self,
        state: SymbolState
    ) -> None:
        """
        Update existing active market state.
        """

        if state.symbol not in self._active_symbols:
            raise ValueError(
                f"Symbol {state.symbol} is not active"
            )

        self._registry.update(state)

        # Synchronization with storage layer
        if self._repository:
            self._repository.save(state)

    def get_market_state(
        self,
        symbol: str
    ) -> Optional[SymbolState]:
        """
        Retrieve current symbol state.
        """

        return self._registry.get(symbol)

    def active_symbols(self) -> List[str]:
        """
        Return active symbols.
        """

        return list(
            self._active_symbols
        )

    def is_active(
        self,
        symbol: str
    ) -> bool:
        """
        Check if symbol is active.
        """

        return symbol in self._active_symbols

    def load_validated_symbol(
        self,
        state: SymbolState
    ) -> None:
        """
        Entry point for exchange adapter.

        BinanceMarketAdapter should convert
        external exchange data into SymbolState
        before calling this method.
        """

        self.activate_symbol(state)
