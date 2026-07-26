import os
from clients.binance_client import BinanceClient

def test_client_creation():
    client = BinanceClient()
    assert client is not None

def test_missing_api_key_blocked():
    old_key = os.environ.pop("BINANCE_API_KEY", None)
    client = BinanceClient()
    try:
        client._headers()
        assert False
    except ValueError:
        assert True
    if old_key:
        os.environ["BINANCE_API_KEY"] = old_key

def test_exchange_info_uses_http_layer():
    """
    Production-grade test verifying dependency injection of HTTP layer.
    """
    class FakeHTTP:
        def get(self, url, headers=None):
            return {
                "status": 200,
                "body": b"{}"
            }

    client = BinanceClient(http_client=FakeHTTP())
    response = client.get_exchange_info()

    assert response["status"] == 200

if __name__ == "__main__":
    test_client_creation()
    test_missing_api_key_blocked()
    test_exchange_info_uses_http_layer()

    print("BinanceClient tests PASSED ✅")
