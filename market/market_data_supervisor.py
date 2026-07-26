class MarketDataSupervisor:
    """
    Production supervisor for MarketDataRuntime.

    Responsibilities:
        - Control runtime lifecycle
        - Monitor runtime state
        - Expose runtime health
        - Delegate runtime operations

    Does NOT contain:
        - Exchange communication
        - Market data generation
        - Scheduler logic
        - Trading decisions
    """

    def __init__(self, runtime):
        self._runtime = runtime

    def start(self) -> None:
        self._runtime.start()

    def stop(self) -> None:
        self._runtime.stop()

    def restart(self) -> dict:
        return self._runtime.restart()

    def state(self) -> dict:
        return self._runtime.state()

    def health(self) -> dict:
        return self._runtime.health()

    def metrics(self) -> dict:
        return self._runtime.metrics()

    def events(self) -> list:
        return self._runtime.events()
