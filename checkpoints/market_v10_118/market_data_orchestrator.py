class MarketDataOrchestrator:
    """
    Production orchestrator for the market data subsystem.

    Responsibilities:
        - Coordinate subsystem startup
        - Coordinate subsystem shutdown
        - Expose subsystem status
        - Delegate operations to the supervisor

    Does NOT contain:
        - Exchange communication
        - Scheduling logic
        - Runtime execution logic
        - Trading decisions
    """

    def __init__(self, supervisor):
        self._supervisor = supervisor

    def start(self):
        self._supervisor.start()

    def stop(self):
        self._supervisor.stop()

    def restart(self):
        return self._supervisor.restart()

    def state(self):
        return self._supervisor.state()

    def health(self):
        return self._supervisor.health()

    def metrics(self):
        return self._supervisor.metrics()

    def events(self):
        return self._supervisor.events()
