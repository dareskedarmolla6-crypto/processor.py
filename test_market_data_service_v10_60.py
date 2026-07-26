import json

from clients.binance_client import BinanceClient
from parsers.binance_market_data_parser import (
    BinanceMarketDataParser
)
from market.market_manager import MarketManager
from services.market_data_service import (
    MarketDataService
)


class TestBinanceClient:

    def get_exchange_info(self):
        return {}


def test_market_data_service_updates_manager():

    client = TestBinanceClient()

    parser = BinanceMarketDataParser()

    manager = MarketManager()


    # Real domain state must be active first
    initial_response = {
        "status": 200,
        "body": json.dumps({
            "symbol": "SERVICE_SYMBOL",
            "price": "100.25"
        }).encode("utf-8")
    }


    initial_state = parser.parse_ticker_price(
        initial_response
    )

    manager.activate_symbol(
        initial_state
    )


    service = MarketDataService(
        client,
        parser,
        manager
    )


    update_response = {
        "status": 200,
        "body": json.dumps({
            "symbol": "SERVICE_SYMBOL",
            "price": "120.50"
        }).encode("utf-8")
    }


    service.update_symbol(
        update_response
    )


    state = manager.get_market_state(
        "SERVICE_SYMBOL"
    )


    assert state.last_price == 120.50
    assert state.exchange == "BINANCE"



def test_market_data_service_rejects_unknown_symbol():

    service = MarketDataService(
        TestBinanceClient(),
        BinanceMarketDataParser(),
        MarketManager()
    )


    response = {
        "status": 200,
        "body": json.dumps({
            "symbol": "UNKNOWN",
            "price": "50.00"
        }).encode("utf-8")
    }


    try:

        service.update_symbol(
            response
        )

        assert False

    except ValueError:
        assert True
