class MarketDataCoordinator:
    """
    Coordinates market data flow.

    Client
        ↓
    Adapter
        ↓
    MarketManager
    """

    def __init__(
        self,
        client,
        adapter,
        manager
    ):
        self._client = client
        self._adapter = adapter
        self._manager = manager

    def update_symbol(
        self,
        symbol: str
    ) -> None:

        ticker = self._client.get_ticker_24h(
            symbol
        )

        state = self._adapter.from_24h(
            ticker
        )

        self._manager.load_validated_symbol(
            state
        )
