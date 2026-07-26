class AutonomousExecutionCommandMonitor:
    """
    Tracks command execution activity.
    """

    def __init__(self):

        self._stats = {
            "total": 0,
            "success": 0,
            "failure": 0
        }


    def record(
        self,
        result
    ):

        self._stats["total"] += 1

        if "error" in result:

            self._stats["failure"] += 1

        else:

            self._stats["success"] += 1



    def snapshot(self):

        return dict(
            self._stats
        )
