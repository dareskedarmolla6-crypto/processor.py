import os
import tempfile

from models.symbol_state import SymbolState
from repositories.sqlite_market_repository import SQLiteMarketRepository


def test_sqlite_save_and_get():

    with tempfile.NamedTemporaryFile(
        suffix=".db"
    ) as db:

        repository = SQLiteMarketRepository(
            db.name
        )

        state = SymbolState(
            symbol="BTCUSDT",
            exchange="BINANCE",
            last_price=123.45,
            bid_price=123.40,
            ask_price=123.50,
            volume=1000.0,
            market_status="ACTIVE"
        )

        repository.save(state)

        loaded = repository.get(
            "BTCUSDT"
        )

        assert loaded is not None
        assert loaded.symbol == "BTCUSDT"
        assert loaded.last_price == 123.45



def test_sqlite_exists():

    with tempfile.NamedTemporaryFile(
        suffix=".db"
    ) as db:

        repository = SQLiteMarketRepository(
            db.name
        )

        state = SymbolState(
            symbol="ETHUSDT",
            exchange="BINANCE",
            last_price=2000.0
        )

        repository.save(state)

        assert repository.exists(
            "ETHUSDT"
        )



def test_sqlite_missing_symbol():

    with tempfile.NamedTemporaryFile(
        suffix=".db"
    ) as db:

        repository = SQLiteMarketRepository(
            db.name
        )

        assert repository.get(
            "UNKNOWN"
        ) is None


if __name__ == "__main__":
    test_sqlite_save_and_get()
    test_sqlite_exists()
    test_sqlite_missing_symbol()

    print(
        "SQLiteMarketRepository tests PASSED ✅"
    )
