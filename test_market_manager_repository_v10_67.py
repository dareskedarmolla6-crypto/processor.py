from market.market_manager import MarketManager
from market.market_state_repository import MarketStateRepository
from models.symbol_state import SymbolState


def test_market_manager_saves_repository():

    repository = MarketStateRepository()

    manager = MarketManager(
        repository=repository
    )

    state = SymbolState(
        exchange="BINANCE",
        symbol="BTCUSDT",
        last_price=50000
    )

    manager.activate_symbol(
        state
    )

    saved = repository.get(
        "BTCUSDT"
    )

    assert saved is not None
    assert saved.last_price == 50000



def test_repository_updates_after_market_update():

    repository = MarketStateRepository()

    manager = MarketManager(
        repository=repository
    )

    state = SymbolState(
        exchange="BINANCE",
        symbol="ETHUSDT",
        last_price=2000
    )

    manager.activate_symbol(
        state
    )

    updated = SymbolState(
        exchange="BINANCE",
        symbol="ETHUSDT",
        last_price=2500
    )

    manager.update_market_state(
        updated
    )

    saved = repository.get(
        "ETHUSDT"
    )

    assert saved.last_price == 2500
