from market.market_data_runtime import MarketDataRuntime


class StubScheduler:

    def run_once(self, symbols):
        pass



def test_runtime_restart_recovers():

    runtime = MarketDataRuntime(
        StubScheduler()
    )

    runtime.start()

    runtime.stop()

    runtime.restart()

    state = runtime.state()

    assert state["status"] == "RUNNING"
    assert runtime.running is True



def test_restart_keeps_cycle_count():

    runtime = MarketDataRuntime(
        StubScheduler()
    )

    runtime.start()

    runtime.run_loop(
        ["BTCUSDT"],
        cycles=3
    )

    before = runtime.state()["cycles"]

    runtime.restart()

    after = runtime.state()["cycles"]

    assert before == after
