class AutonomousExecutionStateStore:
    """
    Central execution state storage layer.
    """

    def __init__(self):

        self._state = {
            "executions": 0,
            "recoveries": 0,
            "health": None,
            "metrics": {},
            "events": 0
        }


    def update_health(
        self,
        health
    ):

        self._state["health"] = health


    def update_metrics(
        self,
        metrics
    ):

        self._state["metrics"] = metrics


    def update_event_count(
        self,
        count
    ):

        self._state["events"] = count


    def increment_execution(self):

        self._state["executions"] += 1


    def increment_recovery(self):

        self._state["recoveries"] += 1


    def snapshot(self):
        """
        Return a copy of the current state snapshot.
        """

        return self._state.copy()


    # [ማስተካከያ] የቀድሞውን ስቴት መልሶ ለመጫን የገባ አዲስ የፕሮዳክሽን ሜቶድ 🚀
    def restore(
        self,
        state
    ) -> bool:
        """
        Restore the execution state from a snapshot.
        """

        if not state:
            return False

        self._state = dict(state)

        return True
