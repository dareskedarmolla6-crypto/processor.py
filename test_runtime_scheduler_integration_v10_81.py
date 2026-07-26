from market.market_data_runtime import MarketDataRuntime


class StubScheduler:

    def __init__(self):
        self.calls = []

    def run_once(self, symbols):
        self.calls.append(symbols)



def test_runtime_scheduler_integration():

    scheduler = StubScheduler()

    runtime = MarketDataRuntime(
        scheduler
    )

    runtime.start()

    runtime.run_loop(
        [
            "BTCUSDT",
            "ETHUSDT"
        ],
        cycles=2
    )

    assert scheduler.calls == [
        [
            "BTCUSDT",
            "ETHUSDT"
        ],
        [
            "BTCUSDT",
            "ETHUSDT"
        ]
    ]



def test_runtime_stop_blocks_execution():

    scheduler = StubScheduler()

    runtime = MarketDataRuntime(
        scheduler
    )

    runtime.start()

    runtime.stop()

    try:
        runtime.run_loop(
            [
                "BTCUSDT"
            ],
            cycles=1
        )

        assert False

    except RuntimeError:
        assert True



if __name__ == "__main__":

    test_runtime_scheduler_integration()
    test_runtime_stop_blocks_execution()

    print(
        "Runtime Scheduler Integration Tests PASSED ✅"
    )
