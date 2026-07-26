from models.symbol_state import SymbolState
from market.market_manager import MarketManager
from repositories.sqlite_market_repository import SQLiteMarketRepository


def test_full_market_persistence_flow():

    repository = SQLiteMarketRepository(
        "full_market_persistence_test.db"
    )

    manager = MarketManager(
        repository=repository
    )

    state = SymbolState(
        symbol="BTCUSDT",
        exchange="BINANCE",
        last_price=60000.0,
        bid_price=59999.0,
        ask_price=60001.0,
        volume=2500.0,
        market_status="ACTIVE"
    )

    # Validated state enters manager
    manager.load_validated_symbol(
        state
    )

    # Verify memory layer
    memory_state = manager.get_market_state(
        "BTCUSDT"
    )

    assert memory_state is not None
    assert memory_state.last_price == 60000.0


    # Verify persistence layer
    database_state = repository.get(
        "BTCUSDT"
    )

    assert database_state is not None
    assert database_state.symbol == "BTCUSDT"
    assert database_state.last_price == 60000.0



def test_full_flow_rejects_invalid_symbol():
    """
    V10.73: Verifies that SymbolState acts as a fail-fast gatekeeper
    and rejects empty symbols immediately during initialization.
    """
    try:
        # ባዶ symbol በመላክ ሞዴሉ እራሱን እንዲከላከል እናስገድደዋለን
        SymbolState(
            symbol="",
            exchange="BINANCE"
        )
        assert False

    except ValueError:
        # የምንጠብቀው የValueError ስህተት ስለመጣ ሙከራው በትክክል ያልፋል
        assert True



if __name__ == "__main__":

    test_full_market_persistence_flow()
    test_full_flow_rejects_invalid_symbol()

    print(
        "Full Market Persistence Flow Tests PASSED ✅"
    )
