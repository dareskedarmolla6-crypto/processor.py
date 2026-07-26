from market.market_data_runtime import MarketDataRuntime


class StubScheduler:

    def __init__(self):
        self.calls = []

    def run_once(self, symbols):
        self.calls.append(symbols)



def test_runtime_runs_loop_once():

    scheduler = StubScheduler()

    runtime = MarketDataRuntime(
        scheduler
    )

    runtime.start()

    runtime.run_loop(
        ["BTCUSDT"],
        cycles=1
    )

    assert scheduler.calls == [
        ["BTCUSDT"]
    ]



def test_runtime_loop_requires_running():

    scheduler = StubScheduler()

    runtime = MarketDataRuntime(
        scheduler
    )

    try:
        runtime.run_loop(
            ["BTCUSDT"],
            cycles=1
        )

        assert False

    except RuntimeError:
        assert True
