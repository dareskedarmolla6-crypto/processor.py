from market.market_data_runtime import MarketDataRuntime


class StubScheduler:

    def run_once(self, symbols):
        pass


def test_runtime_health_initial():

    runtime = MarketDataRuntime(
        StubScheduler()
    )

    health = runtime.health()

    assert health["status"] == "STOPPED"
    assert health["healthy"] is False



def test_runtime_health_after_start():

    runtime = MarketDataRuntime(
        StubScheduler()
    )

    runtime.start()

    health = runtime.health()

    assert health["status"] == "RUNNING"
    assert health["healthy"] is True



def test_runtime_health_after_error():

    class FailingScheduler:

        def run_once(self, symbols):
            raise Exception("scheduler failed")


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


    health = runtime.health()

    assert health["status"] == "ERROR"
    assert health["healthy"] is False
