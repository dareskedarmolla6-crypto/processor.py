class AutonomousExecutionRecoveryFeedbackLoop:
    """
    Stores recovery optimization feedback.
    """

    def __init__(self):

        self._history = []


    def record(
        self,
        result
    ):

        self._history.append(
            dict(result)
        )


    def history(self):

        return list(
            self._history
        )


    def latest(self):

        if not self._history:

            return None

        return self._history[-1]
