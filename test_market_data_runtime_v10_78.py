from market.market_data_runtime import MarketDataRuntime


class StubScheduler:

    def __init__(self):
        self.calls = []

    def run_once(self, symbols):
        self.calls.append(symbols)


def test_runtime_executes_cycle():

    scheduler = StubScheduler()

    runtime = MarketDataRuntime(
        scheduler
    )

    runtime.run_cycle(
        [
            "BTCUSDT",
            "ETHUSDT"
        ]
    )

    assert scheduler.calls == [
        [
            "BTCUSDT",
            "ETHUSDT"
        ]
    ]


def test_runtime_rejects_empty_symbols():

    scheduler = StubScheduler()

    runtime = MarketDataRuntime(
        scheduler
    )

    try:
        runtime.run_cycle([])

        assert False

    except ValueError:
        assert True


if __name__ == "__main__":

    test_runtime_executes_cycle()
    test_runtime_rejects_empty_symbols()

    print(
        "MarketDataRuntime Tests PASSED ✅"
    )
