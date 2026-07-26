from market.market_data_runtime import MarketDataRuntime


class StubScheduler:

    def run_once(self, symbols):
        pass



def test_runtime_start():

    runtime = MarketDataRuntime(
        StubScheduler()
    )

    assert runtime.running is False

    runtime.start()

    assert runtime.running is True



def test_runtime_stop():

    runtime = MarketDataRuntime(
        StubScheduler()
    )

    runtime.start()

    assert runtime.running is True

    runtime.stop()

    assert runtime.running is False



if __name__ == "__main__":

    test_runtime_start()
    test_runtime_stop()

    print(
        "MarketDataRuntime Lifecycle Tests PASSED ✅"
    )
