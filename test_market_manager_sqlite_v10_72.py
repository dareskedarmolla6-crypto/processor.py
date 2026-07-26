from models.symbol_state import SymbolState
from market.market_manager import MarketManager
from repositories.sqlite_market_repository import SQLiteMarketRepository


def test_market_manager_saves_to_sqlite():

    repository = SQLiteMarketRepository(
        "market_manager_test.db"
    )

    manager = MarketManager(
        repository=repository
    )

    state = SymbolState(
        symbol="BTCUSDT",
        exchange="BINANCE",
        last_price=50000.0,
        bid_price=49999.0,
        ask_price=50001.0,
        market_status="ACTIVE"
    )

    manager.activate_symbol(
        state
    )

    stored = repository.get(
        "BTCUSDT"
    )

    assert stored is not None
    assert stored.symbol == "BTCUSDT"
    assert stored.last_price == 50000.0



def test_market_manager_updates_sqlite():

    repository = SQLiteMarketRepository(
        "market_manager_update_test.db"
    )

    manager = MarketManager(
        repository=repository
    )

    initial_state = SymbolState(
        symbol="ETHUSDT",
        exchange="BINANCE",
        last_price=2000.0
    )

    manager.activate_symbol(
        initial_state
    )


    updated_state = SymbolState(
        symbol="ETHUSDT",
        exchange="BINANCE",
        last_price=2100.0
    )

    manager.update_market_state(
        updated_state
    )


    stored = repository.get(
        "ETHUSDT"
    )

    assert stored.last_price == 2100.0



if __name__ == "__main__":

    test_market_manager_saves_to_sqlite()
    test_market_manager_updates_sqlite()

    print(
        "MarketManager SQLite Integration Tests PASSED ✅"
    )
