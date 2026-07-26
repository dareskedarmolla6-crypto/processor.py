from market.market_data_runtime import MarketDataRuntime


class StubScheduler:

    def run_once(self, symbols):
        pass


def test_runtime_logs_cycle():

    logs = []

    runtime = MarketDataRuntime(
        StubScheduler(),
        logger=logs.append
    )

    runtime.start()

    runtime.run_loop(
        ["BTCUSDT"],
        cycles=1
    )

    assert len(logs) > 0


def test_runtime_logs_error():

    logs = []

    class FailingScheduler:

        def run_once(self, symbols):
            raise Exception("failure")

    runtime = MarketDataRuntime(
        FailingScheduler(),
        logger=logs.append
    )

    runtime.start()

    try:
        runtime.run_loop(
            ["BTCUSDT"],
            cycles=1
        )
    except Exception:
        pass

    assert len(logs) > 0
