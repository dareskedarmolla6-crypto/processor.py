from clients.binance_market_data_client import BinanceMarketDataClient


class StubHTTPTransport:

    def __init__(self):
        self.url = None

    def get(self, url):
        self.url = url
        return {
            "status": 200,
            "body": b"{}"
        }


class StubBinanceClient:

    BASE_URL = "https://api.binance.com"

    def __init__(self):
        self.http = StubHTTPTransport()



def test_ticker_price_endpoint():

    client = StubBinanceClient()

    market_client = BinanceMarketDataClient(
        client
    )

    market_client.get_ticker_price(
        "TEST_SYMBOL"
    )

    assert (
        client.http.url
        ==
        "https://api.binance.com/api/v3/ticker/price?symbol=TEST_SYMBOL"
    )



def test_ticker_24h_endpoint():

    client = StubBinanceClient()

    market_client = BinanceMarketDataClient(
        client
    )

    market_client.get_ticker_24h(
        "TEST_SYMBOL"
    )

    assert (
        client.http.url
        ==
        "https://api.binance.com/api/v3/ticker/24hr?symbol=TEST_SYMBOL"
    )
