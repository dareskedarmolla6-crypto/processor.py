from market.market_state_repository import MarketStateRepository
from models.symbol_state import SymbolState


def test_repository_save_and_get():

    repository = MarketStateRepository()

    state = SymbolState(
        exchange="BINANCE",
        symbol="BTCUSDT",
        last_price=100.5
    )

    repository.save(
        state
    )

    result = repository.get(
        "BTCUSDT"
    )

    assert result is not None
    assert result.symbol == "BTCUSDT"
    assert result.last_price == 100.5



def test_repository_missing_symbol():

    repository = MarketStateRepository()

    result = repository.get(
        "UNKNOWN"
    )

    assert result is None



def test_repository_exists():

    repository = MarketStateRepository()

    state = SymbolState(
        exchange="BINANCE",
        symbol="ETHUSDT"
    )

    repository.save(
        state
    )

    assert repository.exists(
        "ETHUSDT"
    )


if __name__ == "__main__":
    test_repository_save_and_get()
    test_repository_missing_symbol()
    test_repository_exists()

    print(
        "MarketStateRepository tests PASSED ✅"
    )
