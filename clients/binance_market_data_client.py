from typing import Dict, Any

from clients.binance_client import BinanceClient


class BinanceMarketDataClient:
    """
    Production Binance market data client.

    Responsibilities:
    - Retrieve real market data from Binance
    - Expose raw validated responses

    Does NOT contain:
    - Trading decisions
    - Indicators
    - Strategy logic
    - Risk logic
    """

    def __init__(
        self,
        client: BinanceClient
    ):
        self.client = client


    def _parse_response(
        self,
        response: Dict[str, Any]
    ) -> Dict[str, Any]:

        if response.get("status") != 200:
            raise RuntimeError(
                f"Binance API error: {response}"
            )

        return response


    def get_ticker_price(
        self,
        symbol: str
    ) -> Dict[str, Any]:
        """
        Retrieve single symbol ticker price.

        Symbol comes from validated
        SymbolRegistry flow.
        """

        url = (
            f"{self.client.BASE_URL}"
            f"/api/v3/ticker/price"
            f"?symbol={symbol}"
        )

        response = self.client.http.get(
            url
        )

        return self._parse_response(
            response
        )


    def get_ticker_24h(
        self,
        symbol: str
    ) -> Dict[str, Any]:
        """
        Retrieve single symbol 24h market statistics.
        """

        url = (
            f"{self.client.BASE_URL}"
            f"/api/v3/ticker/24hr"
            f"?symbol={symbol}"
        )

        response = self.client.http.get(
            url
        )

        return self._parse_response(
            response
        )


    def get_all_ticker_24h(
        self
    ) -> Dict[str, Any]:
        """
        Retrieve all Binance 24h market statistics.

        Used by symbol quality selection layer.

        Exchange request only.
        Does NOT contain:
        - Filtering rules
        - Trading decisions
        - Risk logic
        """

        url = (
            f"{self.client.BASE_URL}"
            "/api/v3/ticker/24hr"
        )

        response = self.client.http.get(
            url
        )

        return self._parse_response(
            response
        )
