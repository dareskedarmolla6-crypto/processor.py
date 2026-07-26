from clients.binance_symbol_client import (
    BinanceSymbolClient
)

from parsers.binance_exchange_parser import (
    BinanceExchangeParser
)

from registry.symbol_registry import (
    SymbolRegistry
)

from market.symbol_activation_policy import (
    SymbolActivationPolicy
)


class SymbolDiscoveryService:
    """
    Production symbol discovery service.

    Responsibilities:
    - Retrieve exchange symbols
    - Parse exchange response
    - Load symbols into registry
    - Filter approved symbols using activation policy

    Does NOT contain:
    - Trading logic
    - Market data updates
    - Strategy logic
    """

    # [ማስተካከያ] አሰላለፉ (Indentation) አሁን በትክክል 4 ስፔስ ሆኗል ✅
    def __init__(
        self,
        client: BinanceSymbolClient,
        parser: BinanceExchangeParser,
        registry: SymbolRegistry,
        policy: SymbolActivationPolicy
    ):
        self.client = client
        self.parser = parser
        self.registry = registry
        self.policy = policy


    def discover(self) -> list[str]:
        """
        Discover, register and approve exchange symbols.
        """

        response = (
            self.client
            .get_exchange_info()
        )

        symbols = (
            self.parser
            .parse(response)
        )

        self.registry.load_symbols(
            symbols
        )

        return self.policy.filter(
            symbols
        )
