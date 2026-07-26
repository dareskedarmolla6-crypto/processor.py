from market.market_data_container import MarketDataContainer


class MarketDataServiceEntry:
    """
    Production entry point for market data subsystem.

    Responsibilities:
        - Create production container
        - Start application lifecycle
        - Stop application lifecycle
        - Expose application state

    Does NOT contain:
        - Market data logic
        - Exchange communication
        - Scheduler logic
        - Trading decisions
    """

    def __init__(self, scheduler):

        self._container = MarketDataContainer(
            scheduler
        )

        self._application = (
            self._container.application
        )

    def start(self):
        """
        Start market data subsystem.
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
