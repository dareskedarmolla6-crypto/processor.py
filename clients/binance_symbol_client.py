import json
from typing import Dict, Any

from clients.binance_client import BinanceClient


class BinanceSymbolClient:
    """
    Production Binance symbol discovery client.

    Responsibilities:
    - Retrieve exchangeInfo from Binance
    - Decode HTTP envelope body and extract parsed JSON

    Does NOT contain:
    - Symbol filtering
    - Trading decisions
    - Registry management
    """

    def __init__(
        self,
        client: BinanceClient
    ):
        self.client = client


    def get_exchange_info(
        self
    ) -> Dict[str, Any]:
        """
        Retrieve Binance exchange information.
        """

        url = (
            f"{self.client.BASE_URL}"
            "/api/v3/exchangeInfo"
        )

        # 1. ጥሬ የ HTTP ኤንቨሎፕ (status, body) ከትራንስፖርት ንብርብሩ ይቀበላል
        response = self.client.http.get(
            url
        )

        # 2. [ማስተካከያ] የ bytes ውሂቡን ፈትቶ ንጹሕ JSON Dictionary ወደ ፓርሰሩ ይልካል ✅
        return json.loads(
            response["body"].decode("utf-8")
        )
