from registry.symbol_registry import SymbolRegistry


class BinanceMarketAdapter:
    """
    Adapter between Binance exchange layer
    and FSE market domain layer.

    Responsibility:
    - Expose exchange symbols to market layer
    - Provide clean market interface

    Not responsible for:
    - Trading decisions
    - Strategy
    - Risk management
    """


    def __init__(
        self,
        symbol_registry: SymbolRegistry
    ):
        self.symbol_registry = symbol_registry


    def get_available_symbols(self):
        """
        Return validated symbols
        from SymbolRegistry.
        """

        return self.symbol_registry.get_trading_symbols()


    def get_symbol(
        self,
        symbol: str
    ):
        """
        Retrieve single symbol metadata.
        """

        return self.symbol_registry.get_symbol(
            symbol
        )
