from market.symbol_feed_manager import SymbolFeedManager
from market.symbol_registry import SymbolRegistry
from models.symbol_state import SymbolState


class StubScheduler:

    def __init__(self):
        self.symbols = None

    def run_cycle(self, symbols):
        self.symbols = symbols



def test_symbol_feed_manager_reads_registry():

    registry = SymbolRegistry()

    registry.register(
        SymbolState(
            exchange="BINANCE",
            symbol="BTCUSDT"
        )
    )

    scheduler = StubScheduler()

    manager = SymbolFeedManager(
        registry,
        scheduler
    )

    manager.run_feed_cycle()

    assert scheduler.symbols == [
        "BTCUSDT"
    ]



def test_symbol_feed_manager_rejects_empty_registry():

    registry = SymbolRegistry()

    scheduler = StubScheduler()

    manager = SymbolFeedManager(
        registry,
        scheduler
    )

    try:
        manager.run_feed_cycle()
        assert False

    except ValueError:
        assert True
