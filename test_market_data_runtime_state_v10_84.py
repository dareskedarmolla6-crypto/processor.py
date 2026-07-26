from market.market_data_runtime import MarketDataRuntime


class StubScheduler:

    def run_once(self, symbols):
        pass



def test_runtime_initial_state():

    runtime = MarketDataRuntime(
        StubScheduler()
    )

    state = runtime.state()

    assert state["status"] == "STOPPED"
    assert state["cycles"] == 0



def test_runtime_updates_state_after_cycle():

    runtime = MarketDataRuntime(
        StubScheduler()
    )

    runtime.start()

    runtime.run_loop(
        ["BTCUSDT"],
        cycles=2
    )

    state = runtime.state()

    assert state["status"] == "RUNNING"
    assert state["cycles"] == 2
    assert state["last_error"] is None



def test_runtime_tracks_error():

    class FailingScheduler:

        def run_once(self, symbols):
            raise Exception(
                "update failed"
            )


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


    state = runtime.state()

    assert state["status"] == "ERROR"
    assert state["last_error"] == "update failed"
