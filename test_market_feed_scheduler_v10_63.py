from market.market_feed_scheduler import (
    MarketFeedScheduler
)


class StubFeedService:
    """
    Isolated dependency contract test.
    """

    def __init__(self):
        self.received_symbols = None


    def update_symbols(
        self,
        symbols
    ):
        self.received_symbols = symbols



def test_scheduler_forwards_symbols():

    service = StubFeedService()

    scheduler = MarketFeedScheduler(
        service
    )

    symbols = [
        "BTCUSDT",
        "ETHUSDT"
    ]

    scheduler.run_cycle(
        symbols
    )

    assert (
        service.received_symbols
        ==
        symbols
    )



def test_scheduler_rejects_empty_symbols():

    service = StubFeedService()

    scheduler = MarketFeedScheduler(
        service
    )


    try:
        scheduler.run_cycle(
            []
        )

        assert False

    except ValueError:
        assert True
