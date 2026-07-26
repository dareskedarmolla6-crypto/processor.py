class MarketDataBootstrap:
    """
    Production bootstrap layer.

    Responsibilities:
        - Discover valid exchange symbols
        - Activate initial market states
        - Prepare runtime environment

    Does NOT contain:
        - Trading logic
        - Strategy logic
        - Risk logic
    """

    def __init__(
        self,
        symbol_discovery,
        symbol_activator
    ):
        self._symbol_discovery = symbol_discovery
        self._symbol_activator = symbol_activator


    def initialize(self) -> None:
        """
        Execute complete pre-flight initialization chain.

        Flow:
            Discovery
              |
            Activation
        """

        symbols = (
            self._symbol_discovery.discover()
        )

        self._symbol_activator.activate(
            symbols
        )
