import os
from typing import Dict, Any
from transport.http_client import HTTPClient

class BinanceClient:
    """
    Low-level Binance API client.

    Responsibilities:
    - Handle API communication
    - Manage authentication headers
    - Return validated exchange responses

    It does NOT contain:
    - Trading decisions
    - Risk logic
    - Portfolio logic
    """

    BASE_URL = "https://api.binance.com"

    def __init__(
        self,
        api_key: str | None = None,
        api_secret: str | None = None,
        http_client: HTTPClient | None = None
    ):
        self.api_key = (
            api_key
            or os.getenv("BINANCE_API_KEY")
        )

        self.api_secret = (
            api_secret
            or os.getenv("BINANCE_API_SECRET")
        )

        # Dependency Injection: 
        # http_client መጠቀም ከተፈለገ ያንን እንጠቀማለን፣ ካልሆነ ግን ነባሪውን (default) እንፈጥራለን
        self.http = (
            http_client
            or HTTPClient()
        )

    def _headers(self) -> Dict[str, str]:
        """
        Build authentication headers.
        """

        if not self.api_key:
            raise ValueError(
                "Missing Binance API key"
            )

        return {
            "X-MBX-APIKEY": self.api_key
        }

    def get_exchange_info(self) -> Dict[str, Any]:
        """
        Retrieve exchange information.
        """
        # አሁን self.http በመጠቀም እውነተኛ ጥያቄ ማቅረብ እንችላለን
        return self.http.get(f"{self.BASE_URL}/api/v3/exchangeInfo")
