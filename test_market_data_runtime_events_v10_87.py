from market.market_data_runtime import MarketDataRuntime


class StubScheduler:

    def run_once(self, symbols):
        return None


def test_runtime_event_history():

    runtime = MarketDataRuntime(
        StubScheduler()
    )

    runtime.start()
    runtime.stop()

    events = runtime.events()

    assert "runtime_started" in events
    assert "runtime_stopped" in events


def test_cycle_events_recorded():

    runtime = MarketDataRuntime(
        StubScheduler()
    )

    runtime.start()

    runtime.run_loop(
        ["BTCUSDT"],
        cycles=2
    )

    events = runtime.events()

    assert events.count(
        "cycle_started"
    ) == 2

    assert events.count(
        "cycle_completed"
    ) == 2


def test_error_event_recorded():

    class ErrorScheduler:

        def run_once(self, symbols):
            raise Exception(
                "scheduler failure"
            )

    runtime = MarketDataRuntime(
        ErrorScheduler()
    )

    runtime.start()

    try:
        runtime.run_loop(
            ["BTCUSDT"],
            cycles=1
        )

    except Exception:
        pass

    events = runtime.events()

    assert "runtime_error" in events
