from market.symbol_registry import SymbolRegistry
from market.symbol_feed_manager import SymbolFeedManager
from market.market_feed_scheduler import MarketFeedScheduler
from models.symbol_state import SymbolState


class StubFeedService:
    """
    Test-only service contract.
    """

    def __init__(self):
        self.received_symbols = None

    def update_symbols(self, symbols):
        self.received_symbols = symbols



def test_full_market_data_flow():

    # Registry layer
    registry = SymbolRegistry()

    registry.register(
        SymbolState(
            exchange="BINANCE",
            symbol="BTCUSDT"
        )
    )


    # Feed service layer
    feed_service = StubFeedService()


    # Scheduler layer
    scheduler = MarketFeedScheduler(
        feed_service
    )


    # Manager layer
    manager = SymbolFeedManager(
        registry,
        scheduler
    )


    # Execute complete flow
    manager.run_feed_cycle()


    assert (
        feed_service.received_symbols
        ==
        ["BTCUSDT"]
    )



def test_full_flow_requires_symbols():

    registry = SymbolRegistry()

    feed_service = StubFeedService()

    scheduler = MarketFeedScheduler(
        feed_service
    )

    manager = SymbolFeedManager(
        registry,
        scheduler
    )


    try:
        manager.run_feed_cycle()
        assert False

    except ValueError:
        assert True
