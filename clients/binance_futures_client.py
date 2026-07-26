import os
import time
import hmac
import hashlib
import urllib.parse
import logging
from typing import Dict, Any
from dotenv import load_dotenv
from transport.http_client import HTTPClient

load_dotenv()

logger = logging.getLogger(__name__)


class BinanceFuturesClient:
    """
    Production Binance Futures API client.

    Responsibilities:
    - Futures order communication
    - Leverage management
    - Position information retrieval

    Does NOT contain:
    - Trading decisions
    - Risk logic
    - Strategy logic
    """

    BASE_URL = "https://fapi.binance.com"

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
        self.http = (
            http_client
            or HTTPClient()
        )

    def _headers(self) -> Dict[str, str]:
        if not self.api_key:
            raise ValueError(
                "Missing Binance API key"
            )
        return {
            "X-MBX-APIKEY": self.api_key
        }

    def _signed_params(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate Binance HMAC SHA256 signature and attach timestamp.
        """
        if not self.api_secret:
            raise ValueError(
                "Missing Binance API secret for signed request"
            )

        payload["timestamp"] = int(time.time() * 1000)

        query = urllib.parse.urlencode(payload)

        signature = hmac.new(
            self.api_secret.encode(),
            query.encode(),
            hashlib.sha256
        ).hexdigest()

        payload["signature"] = signature

        return payload

    def futures_create_order(
        self,
        symbol: str,
        side: str,
        type: str,
        quantity: float,
        newClientOrderId: str | None = None
    ):
        """
        Futures market order endpoint with HMAC SHA256 signature.
        """
        payload = {
            "symbol": symbol,
            "side": side,
            "type": type,
            "quantity": quantity,
        }

        if newClientOrderId:
            payload["newClientOrderId"] = newClientOrderId

        payload = self._signed_params(payload)

        logger.info(
            f"Futures order request: {payload}"
        )

        return self.http.post(
            f"{self.BASE_URL}/fapi/v1/order",
            headers=self._headers(),
            data=payload
        )

    def futures_change_leverage(
        self,
        symbol: str,
        leverage: int
    ):
        payload = {
            "symbol": symbol,
            "leverage": leverage
        }

        payload = self._signed_params(payload)

        return self.http.post(
            f"{self.BASE_URL}/fapi/v1/leverage",
            headers=self._headers(),
            data=payload
        )

    def futures_position_information(
        self,
        symbol: str
    ):
        payload = {
            "symbol": symbol
        }

        payload = self._signed_params(payload)

        query = urllib.parse.urlencode(payload)

        return self.http.get(
            f"{self.BASE_URL}/fapi/v2/positionRisk?{query}",
            headers=self._headers()
        )

    def futures_get_order(
        self,
        symbol: str,
        orderId: int
    ):
        return self.http.get(
            f"{self.BASE_URL}/fapi/v1/order"
            f"?symbol={symbol}&orderId={orderId}",
            headers=self._headers()
        )
