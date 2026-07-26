class MarketDataApplication:
    """
    Production application bootstrap layer.

    Responsibilities:
        - Own application lifecycle
        - Start market data subsystem
        - Stop market data subsystem

    Does NOT contain:
        - Market data logic
        - Runtime logic
        - Exchange communication
    """

    def __init__(self, orchestrator):
        self._orchestrator = orchestrator

    def start(self):
        self._orchestrator.start()

    def stop(self):
        self._orchestrator.stop()

    def restart(self):
        return self._orchestrator.restart()

    def state(self):
        return self._orchestrator.state()

    def health(self):
        return self._orchestrator.health()
