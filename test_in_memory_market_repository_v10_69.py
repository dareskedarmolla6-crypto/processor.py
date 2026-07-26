from repositories.in_memory_market_repository import (
    InMemoryMarketRepository,
)
from models.symbol_state import SymbolState


def test_save_and_get():

    repository = InMemoryMarketRepository()

    state = SymbolState(
        exchange="BINANCE",
        symbol="BTCUSDT",
        last_price=65000.0
    )

    repository.save(state)

    result = repository.get("BTCUSDT")

    assert result is not None
    assert result.last_price == 65000.0


def test_exists():

    repository = InMemoryMarketRepository()

    repository.save(
        SymbolState(
            exchange="BINANCE",
            symbol="ETHUSDT"
        )
    )

    assert repository.exists("ETHUSDT")
    assert not repository.exists("XRPUSDT")
