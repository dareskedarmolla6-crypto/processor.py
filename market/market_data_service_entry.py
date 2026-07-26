from market.market_data_container import MarketDataContainer


class MarketDataServiceEntry:
    """
    Production entry point for market data subsystem.

    Responsibilities:
        - Create production runtime container
        - Execute explicit bootstrap when requested
        - Start application lifecycle
        - Stop application lifecycle
        - Expose application state

    Does NOT contain:
        - Market data logic
        - Symbol discovery logic
        - Exchange communication
        - Trading decisions
    """

    def __init__(
        self,
        scheduler=None
    ):

        self._container = MarketDataContainer(
            scheduler=scheduler
        )

        self._bootstrap = (
            self._container.bootstrap
            if hasattr(self._container, "bootstrap")
            else None
        )

        self._application = (
            self._container.application
        )


    def initialize(self):
        """
        Execute production bootstrap explicitly.

        This may communicate with exchange APIs.
        It is intentionally separated from lifecycle start.
        """

        if self._bootstrap is None:
            raise RuntimeError(
                "Bootstrap is not configured"
            )

        self._bootstrap.initialize()


    def start(self):
        """
        Start market data application lifecycle.

        Does NOT call bootstrap.
        """

        self._application.start()


    def stop(self):
        """
        Stop market data subsystem.
        """

        self._application.stop()


    def state(self):
        """
        Return application state.
        """

        return self._application.state()
