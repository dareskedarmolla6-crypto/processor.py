class AutonomousExecutionObservability:
    """
    Unified observability layer.
    """

    def __init__(
        self,
        monitor,
        state_store,
        audit
    ):

        self.monitor = monitor
        self.state_store = state_store
        self.audit = audit


    def snapshot(self):

        return {
            "metrics": self.monitor.snapshot(),
            "state": self.state_store.snapshot(),
            "events": self.audit.history()
        }
