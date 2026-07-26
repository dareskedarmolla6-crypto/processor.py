from models.symbol_state import SymbolState
from market.market_manager import MarketManager


def test_activate_and_get():
    manager = MarketManager()

    state = SymbolState(
        symbol="BTCUSDT",
        exchange="BINANCE",
        last_price=60000.0
    )

    manager.activate_symbol(state)

    result = manager.get_market_state("BTCUSDT")

    assert result is not None
    assert result.symbol == "BTCUSDT"
    assert manager.is_active("BTCUSDT")


def test_update_market_state():
    manager = MarketManager()

    state = SymbolState(
        symbol="ETHUSDT",
        exchange="BINANCE",
        last_price=3000.0
    )

    manager.activate_symbol(state)

    updated = SymbolState(
        symbol="ETHUSDT",
        exchange="BINANCE",
        last_price=3200.0
    )

    manager.update_market_state(updated)

    result = manager.get_market_state("ETHUSDT")

    assert result.last_price == 3200.0


def test_invalid_update():
    manager = MarketManager()

    state = SymbolState(
        symbol="SOLUSDT",
        exchange="BINANCE",
        last_price=150.0
    )

    try:
        manager.update_market_state(state)
        assert False
    except ValueError:
        assert True


def test_deactivate():
    manager = MarketManager()

    state = SymbolState(
        symbol="BNBUSDT",
        exchange="BINANCE",
        last_price=500.0
    )

    manager.activate_symbol(state)
    manager.deactivate_symbol("BNBUSDT")

    assert not manager.is_active("BNBUSDT")
    assert manager.get_market_state("BNBUSDT") is None


if __name__ == "__main__":
    test_activate_and_get()
    test_update_market_state()
    test_invalid_update()
    test_deactivate()

    print("MarketManager tests PASSED")
