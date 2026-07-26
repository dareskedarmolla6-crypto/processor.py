from market.market_data_runtime import MarketDataRuntime


class StubScheduler:

    def run_once(self, symbols):
        return None


class ErrorScheduler:

    def run_once(self, symbols):
        raise Exception("scheduler failure")


def test_success_metrics():

    runtime = MarketDataRuntime(
        StubScheduler()
    )

    runtime.start()

    runtime.run_loop(
        ["BTCUSDT"],
        cycles=3
    )

    metrics = runtime.metrics()

    assert metrics["successful_cycles"] == 3
    assert metrics["failed_cycles"] == 0


def test_failure_metrics():

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

    metrics = runtime.metrics()

    assert metrics["successful_cycles"] == 0
    assert metrics["failed_cycles"] == 1


def test_metrics_snapshot_is_copy():

    runtime = MarketDataRuntime(
        StubScheduler()
    )

    metrics = runtime.metrics()

    metrics["successful_cycles"] = 100

    assert runtime.metrics()["successful_cycles"] == 0
