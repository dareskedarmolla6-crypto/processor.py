from models.symbol_state import SymbolState
from market.symbol_registry import SymbolRegistry


def test_register_and_get():
    registry = SymbolRegistry()

    state = SymbolState(
        symbol="BTCUSDT",
        exchange="BINANCE",
        last_price=60000.0
    )

    registry.register(state)

    result = registry.get("BTCUSDT")

    assert result is not None
    assert result.symbol == "BTCUSDT"
    assert result.last_price == 60000.0


def test_update():
    registry = SymbolRegistry()

    state = SymbolState(
        symbol="ETHUSDT",
        exchange="BINANCE",
        last_price=3000.0
    )

    registry.register(state)

    updated = SymbolState(
        symbol="ETHUSDT",
        exchange="BINANCE",
        last_price=3100.0
    )

    registry.update(updated)

    result = registry.get("ETHUSDT")

    assert result.last_price == 3100.0


def test_remove():
    registry = SymbolRegistry()

    state = SymbolState(
        symbol="SOLUSDT",
        exchange="BINANCE",
        last_price=150.0
    )

    registry.register(state)
    registry.remove("SOLUSDT")

    assert registry.get("SOLUSDT") is None


def test_snapshot():
    registry = SymbolRegistry()

    state = SymbolState(
        symbol="BNBUSDT",
        exchange="BINANCE",
        last_price=500.0
    )

    registry.register(state)

    snapshot = registry.snapshot()

    assert "BNBUSDT" in snapshot
    assert snapshot["BNBUSDT"].last_price == 500.0


if __name__ == "__main__":
    test_register_and_get()
    test_update()
    test_remove()
    test_snapshot()

    print("SymbolRegistry tests PASSED")
