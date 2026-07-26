from clients.binance_client import BinanceClient
from clients.binance_market_data_client import BinanceMarketDataClient


class TestHTTPClient:
    """
    Isolated transport contract test dependency.

    This is NOT production exchange code.
    """

    def __init__(self):
        self.last_url = None


    def get(
        self,
        url,
        headers=None
    ):
        self.last_url = url

        return {
            "status": 200,
            "body": b'{"price":"100"}'
        }



def test_market_data_client_price_endpoint():

    http = TestHTTPClient()

    client = BinanceClient(
        api_key="test-key",
        http_client=http
    )

    market_client = BinanceMarketDataClient(
        client
    )

    response = market_client.get_ticker_price(
        "TEST_SYMBOL"
    )

    assert response["status"] == 200
    assert "ticker/price" in http.last_url


def test_market_data_client_24h_endpoint():

    http = TestHTTPClient()

    client = BinanceClient(
        api_key="test-key",
        http_client=http
    )

    market_client = BinanceMarketDataClient(
        client
    )

    response = market_client.get_ticker_24h(
        "TEST_SYMBOL"
    )

    assert response["status"] == 200
    assert "ticker/24hr" in http.last_url
