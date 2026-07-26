from market.market_data_runtime import MarketDataRuntime
from market.sqlite_runtime_event_repository import (
    SQLiteRuntimeEventRepository
)


class StubScheduler:

    def run_once(self, symbols):
        pass


def test_runtime_event_persistence():

    db = "runtime_events_v10_98_test.db"

    repository = SQLiteRuntimeEventRepository(
        db
    )

    runtime = MarketDataRuntime(
        StubScheduler(),
        event_repository=repository
    )

    runtime.start()
    runtime.stop()

    events = repository.load_events()

    assert "runtime_started" in events
    assert "runtime_stopped" in events



def test_runtime_restores_events():

    db = "runtime_events_v10_98_restore.db"

    repository = SQLiteRuntimeEventRepository(
        db
    )

    runtime1 = MarketDataRuntime(
        StubScheduler(),
        event_repository=repository
    )

    runtime1.start()

    runtime2 = MarketDataRuntime(
        StubScheduler(),
        event_repository=repository
    )

    events = runtime2.events()

    assert "runtime_started" in events
