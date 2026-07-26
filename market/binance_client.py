from typing import Dict, Any
import json

from transport.http_client import HTTPClient


class BinanceClient:
    """
    Production Binance market data client.

    Responsibilities:
        - Communicate with Binance public market API
        - Retrieve market ticker data
        - Return raw exchange responses

    Does NOT contain:
        - Trading logic
        - Strategy logic
        - Risk logic
        - Portfolio logic
    """

    BASE_URL = "https://api.binance.com"

    def __init__(
        self,
        http_client: HTTPClient
    ):
        self._http_client = http_client

    def get_ticker_24h(
        self,
        symbol: str
    ) -> Dict[str, Any]:
        """
        Retrieve 24 hour ticker data from Binance.
        Aligned with MarketDataCoordinator interface contract.
        """

        if not symbol:
            raise ValueError(
                "Symbol cannot be empty"
            )

        url = (
            f"{self.BASE_URL}"
            f"/api/v3/ticker/24hr"
            f"?symbol={symbol}"
        )

        response = self._http_client.get(
            url
        )

        if response["status"] != 200:
            raise ConnectionError(
                "Binance API request failed"
            )

        return json.loads(
            response["body"].decode("utf-8")
        )
