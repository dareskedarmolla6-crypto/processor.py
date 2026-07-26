from models.symbol_state import SymbolState
from market.market_manager import MarketManager
from market.market_data_pipeline import MarketDataPipeline


def test_pipeline_updates_market_manager():

    manager = MarketManager()

    state = SymbolState(
        exchange="BINANCE",
        symbol="BTCUSDT",
        last_price=50000.0
    )

    manager.activate_symbol(
        state
    )

    pipeline = MarketDataPipeline(
        manager
    )

    updated_state = SymbolState(
        exchange="BINANCE",
        symbol="BTCUSDT",
        last_price=51000.0
    )

    pipeline.process(
        updated_state
    )

    result = manager.get_market_state(
        "BTCUSDT"
    )

    assert result.last_price == 51000.0



def test_pipeline_rejects_invalid_state():

    manager = MarketManager()

    pipeline = MarketDataPipeline(
        manager
    )

    try:
        pipeline.process(
            "INVALID"
        )
        assert False

    except TypeError:
        assert True
