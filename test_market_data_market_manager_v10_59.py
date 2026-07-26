import json

from parsers.binance_market_data_parser import (
    BinanceMarketDataParser
)

from market.market_manager import MarketManager


def test_market_data_updates_market_manager():

    parser = BinanceMarketDataParser()

    response = {
        "status": 200,
        "body": json.dumps({
            "symbol": "TEST_SYMBOL",
            "price": "250.50"
        }).encode("utf-8")
    }


    # Convert Binance response -> SymbolState
    state = parser.parse_ticker_price(
        response
    )


    manager = MarketManager()


    # Symbol must be active before update
    manager.activate_symbol(
        state
    )


    updated_state = manager.get_market_state(
        "TEST_SYMBOL"
    )


    assert updated_state is not None
    assert updated_state.symbol == "TEST_SYMBOL"
    assert updated_state.last_price == 250.50
    assert updated_state.exchange == "BINANCE"



def test_market_manager_rejects_inactive_symbol():

    parser = BinanceMarketDataParser()

    response = {
        "status": 200,
        "body": json.dumps({
            "symbol": "UNKNOWN_SYMBOL",
            "price": "10.00"
        }).encode("utf-8")
    }


    state = parser.parse_ticker_price(
        response
    )


    manager = MarketManager()


    try:
        manager.update_market_state(
            state
        )

        assert False

    except ValueError:
        assert True
