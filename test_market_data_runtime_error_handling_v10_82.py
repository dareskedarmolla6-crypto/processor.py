from market.market_data_runtime import MarketDataRuntime


class FailingScheduler:

    def run_once(self, symbols):
        raise Exception(
            "Scheduler failure"
        )


def test_runtime_handles_scheduler_error():

    runtime = MarketDataRuntime(
        FailingScheduler()
    )

    runtime.start()

    try:
        runtime.run_loop(
            ["BTCUSDT"],
            cycles=1
        )

        assert False

    except Exception as e:
        assert str(e) == "Scheduler failure"



def test_runtime_remains_running_after_error():

    runtime = MarketDataRuntime(
        FailingScheduler()
    )

    runtime.start()

    try:
        runtime.run_loop(
            ["BTCUSDT"],
            cycles=1
        )

    except Exception:
        pass

    assert runtime.running is True
