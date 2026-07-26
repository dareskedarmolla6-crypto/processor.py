class AutonomousExecutionRecoveryAudit:
    """
    Tracks recovery operations.
    """

    def __init__(self):

        self._events = []


    def record(
        self,
        result
    ):

        self._events.append(
            {
                "type": "RECOVERY",
                "result": result
            }
        )


    def history(self):

        return list(self._events)
