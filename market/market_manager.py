from typing import Optional, List
from models.symbol_state import SymbolState
from market.symbol_registry import SymbolRegistry
from repositories.market_repository import MarketRepository


class MarketManager:
    """
    Production market state coordinator.

    Responsibilities:
        - Manage active market symbols
        - Coordinate validated market state updates
        - Provide market state access layer
        - Dynamic symbol selection via classification scoring

    Exchange connectivity remains outside this class.
    Real exchange adapters push validated state here.
    """

    def __init__(
        self,
        repository: Optional[MarketRepository] = None
    ):
        self._registry = SymbolRegistry()
        self._active_symbols = set()
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

    def active_symbols(
        self
    ) -> List[str]:
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
        """
        self.activate_symbol(state)

    def get_all_market_states(
        self
    ) -> dict:
        """
        Return all active market states.

        Used by production decision layer
        to consume validated market data.
        """
        states = {}

        for symbol in self._active_symbols:
            state = self._registry.get(symbol)

            if state:
                states[symbol] = {
                    "price": state.last_price,
                    "volume": state.volume,
                    "symbol": state.symbol,
                    "exchange": state.exchange,
                    "alpha_score": state.alpha_score,
                    "tradefi_score": state.tradefi_score,
                    "volatility": state.volatility,
                    "liquidity_score": state.liquidity_score,
                    "price_change_percent": state.price_change_percent
                }

        return states

    def select_best_symbol(
        self
    ) -> Optional[str]:
        """
        Select production trading candidate using classification logic.

        Rules:
            - Must be active.
            - Must have valid market state.
            - Must have valid price within low-price trading range (0.00012 to 0.01).
            - Classification score based on:
                Alpha Score (50%) + TradeFi Score (30%) + Volatility (10%) + Liquidity Score (10%)

        No hard-coded symbols.
        Uses only validated market data and dynamic scoring.
        """
        best_symbol = None
        best_score = -1.0

        for symbol in self._active_symbols:
            state = self._registry.get(symbol)

            if state is None:
                continue

            price = getattr(
                state,
                "last_price",
                None
            )

            if price is None:
                continue

            # Trading universe filter: Low price range filter
            if price < 0.00012 or price > 0.01:
                continue

            # Extract classification scores safely
            alpha_score = getattr(state, "alpha_score", 0.0) or 0.0
            tradefi_score = getattr(state, "tradefi_score", 0.0) or 0.0
            volatility = getattr(state, "volatility", 0.0) or 0.0
            liquidity_score = getattr(state, "liquidity_score", 0.0) or 0.0

            # Dynamic classification score calculation
            score = (
                (alpha_score * 0.5)
                + (tradefi_score * 0.3)
                + (volatility * 0.1)
                + (liquidity_score * 0.1)
            )

            if score > best_score:
                best_score = score
                best_symbol = symbol

        return best_symbol

    def state(
        self
    ) -> dict:
        """
        Return runtime manager state summary.
        """
        return {
            "active_symbols": len(
                self._active_symbols
            )
        }
