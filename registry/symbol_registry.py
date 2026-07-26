from typing import Dict, List, Optional


class SymbolRegistry:
    """
    Production symbol registry.

    Responsibility:
    - Store validated exchange symbols
    - Provide lookup operations
    - Prevent duplicate entries

    Not responsible for:
    - Creating symbols
    - Market analysis
    - Trading decisions
    """

    def __init__(self):
        self._symbols: Dict[str, dict] = {}

    def load_symbols(self, symbols: List[dict]) -> None:
        """
        Load symbols coming from ExchangeParser.
        """

        for symbol in symbols:
            self._register(symbol)

    def _register(self, symbol: dict) -> None:
        symbol_name = symbol.get("symbol")

        if not symbol_name:
            raise ValueError(
                "Symbol name missing"
            )

        self._symbols[symbol_name] = symbol

    def get_symbol(
        self,
        symbol_name: str
    ) -> Optional[dict]:

        return self._symbols.get(symbol_name)

    def get_all_symbols(self) -> List[dict]:

        return list(self._symbols.values())

    def count(self) -> int:

        return len(self._symbols)

    def get_trading_symbols(self) -> List[dict]:

        return [
            symbol
            for symbol in self._symbols.values()
            if symbol.get("status") == "TRADING"
        ]
