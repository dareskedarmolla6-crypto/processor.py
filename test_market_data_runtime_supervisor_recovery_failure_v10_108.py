import pytest

from market.market_data_runtime_supervisor import (
    MarketDataRuntimeSupervisor
)


class FailingRuntime:

    def __init__(self):
        self._running = False

    def start(self):
        self._running = True

    def stop(self):
        self._running = False

    def restart(self):
        raise RuntimeError(
            "restart failed"
        )

    def health(self):
        return {
            "status": "ERROR",
            "healthy": False,
            "cycles": 0,
            "last_error": "runtime_error"
        }

    @property
    def running(self):
        return self._running


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


def test_recovery_records_failure_event():

    runtime = FailingRuntime()

    repository = (
        InMemoryEventRepository()
    )

    supervisor = (
        MarketDataRuntimeSupervisor(
            runtime,
            event_repository=repository
        )
    )

    with pytest.raises(
        RuntimeError
    ):
        supervisor.recover()

    assert (
        "recovery_failed"
        in repository.load_events()
    )


def test_recovery_records_started_before_failure():

    runtime = FailingRuntime()

    repository = (
        InMemoryEventRepository()
    )

    supervisor = (
        MarketDataRuntimeSupervisor(
            runtime,
            event_repository=repository
        )
    )

    with pytest.raises(
        RuntimeError
    ):
        supervisor.recover()

    events = repository.load_events()

    assert events[0] == "recovery_started"
    assert events[-1] == "recovery_failed"
