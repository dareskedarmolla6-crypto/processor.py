from datetime import datetime, timezone, timedelta
from models.symbol_state import SymbolState
from market.market_validator import MarketValidator

def test_valid_state():
    state = SymbolState(
        symbol="BTCUSDT",
        exchange="BINANCE",
        last_price=60000.0
    )
    assert state.symbol == "BTCUSDT"
    assert state.last_price == 60000.0

def test_market_validator_accepts_valid_state():
    validator = MarketValidator()
    state = SymbolState(
        symbol="BTCUSDT",
        exchange="BINANCE",
        last_price=60000.0
    )
    assert validator.validate(state) is True

def test_empty_symbol():
    # Structural integrity check (via Model)
    try:
        SymbolState(symbol="", exchange="BINANCE", last_price=60000.0)
        assert False
    except ValueError:
        assert True

def test_invalid_price():
    # Structural integrity check (via Model)
    try:
        SymbolState(symbol="ETHUSDT", exchange="BINANCE", last_price=0)
        assert False
    except ValueError:
        assert True

def test_missing_timezone():
    # Business rule check (via MarketValidator)
    validator = MarketValidator()
    state = SymbolState(
        symbol="SOLUSDT",
        exchange="BINANCE",
        last_price=150.0,
        timestamp=datetime.now() # Naive datetime
    )
    try:
        validator.validate(state)
        assert False
    except ValueError:
        assert True

def test_future_timestamp():
    # Business rule check (via MarketValidator)
    validator = MarketValidator()
    state = SymbolState(
        symbol="BNBUSDT",
        exchange="BINANCE",
        last_price=500.0,
        timestamp=datetime.now(timezone.utc) + timedelta(days=1)
    )
    try:
        validator.validate(state)
        assert False
    except ValueError:
        assert True

if __name__ == "__main__":
    test_valid_state()
    test_market_validator_accepts_valid_state()
    test_empty_symbol()
    test_invalid_price()
    test_missing_timezone()
    test_future_timestamp()

    print("MarketValidator tests PASSED ✅")
