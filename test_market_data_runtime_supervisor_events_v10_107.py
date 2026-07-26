from market.market_data_runtime_supervisor import (
    MarketDataRuntimeSupervisor
)


class FakeRuntime:

    def __init__(self):
        self._running = False


    def start(self):
        self._running = True


    def stop(self):
        self._running = False


    def restart(self):
        self._running = True
        return {
            "status": "RUNNING"
        }


    def health(self):
        return {
            "status": "RUNNING",
            "healthy": True,
            "cycles": 0,
            "last_error": None
        }


    @property
    def running(self):
        return self._running


class UnhealthyRuntime(FakeRuntime):

    def __init__(self):

        super().__init__()

        self.restart_called = False


    def restart(self):

        self.restart_called = True

        self._running = True

        return {
            "status": "RUNNING"
        }


    def health(self):

        if self.restart_called:

            return {
                "status": "RUNNING",
                "healthy": True,
                "cycles": 0,
                "last_error": None
            }


        return {
            "status": "ERROR",
            "healthy": False,
            "cycles": 0,
            "last_error": "runtime_error"
        }


class InMemoryEventRepository:

    def __init__(self):
        self._events = []


    def save_event(
        self,
        event
    ):
        self._events.append(event)


    def load_events(self):
        return self._events.copy()


def test_recovery_records_started_event():

    runtime = FakeRuntime()

    repository = (
        InMemoryEventRepository()
    )

    supervisor = (
        MarketDataRuntimeSupervisor(
            runtime,
            event_repository=repository
        )
    )

    supervisor.recover()

    assert (
        "recovery_started"
        in repository.load_events()
    )


def test_recovery_records_completed_event():

    runtime = UnhealthyRuntime()

    repository = (
        InMemoryEventRepository()
    )

    supervisor = (
        MarketDataRuntimeSupervisor(
            runtime,
            event_repository=repository
        )
    )

    supervisor.recover()

    assert (
        "recovery_completed"
        in repository.load_events()
    )
