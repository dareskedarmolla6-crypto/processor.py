from datetime import datetime, timezone
from typing import Dict, Any
import json

from models.symbol_state import SymbolState


class BinanceMarketDataParser:
    """
    Production Binance market data parser.

    Responsibilities:
    - Validate Binance market response
    - Convert response to SymbolState

    Does NOT contain:
    - Trading decisions
    - Strategy logic
    - Risk logic
    """


    def parse_ticker_price(
        self,
        response: Dict[str, Any]
    ) -> SymbolState:
        """
        Parse Binance ticker price response.
        """

        self._validate_response(response)

        body = response["body"]

        if isinstance(body, bytes):
            body = body.decode("utf-8")

        data = json.loads(body)

        symbol = data.get("symbol")
        price = data.get("price")


        if not symbol:
            raise ValueError(
                "Missing symbol"
            )

        if price is None:
            raise ValueError(
                "Missing price"
            )


        return SymbolState(
            exchange="BINANCE",
            symbol=symbol,
            last_price=float(price),  # እውነተኛውን የዶሜን ሞዴል ኮንትራት ለመጠበቅ ወደ last_price ተቀይሯል
            timestamp=datetime.now(
                timezone.utc
            )
        )


    def parse_ticker_24h(
        self,
        ticker: Dict[str, Any]
    ) -> SymbolState:
        """
        Parse Binance 24h ticker into SymbolState.
        """

        last_price = float(
            ticker["lastPrice"]
        )

        high = float(
            ticker.get(
                "highPrice",
                0
            )
        )

        low = float(
            ticker.get(
                "lowPrice",
                0
            )
        )

        volume = float(
            ticker.get(
                "quoteVolume",
                0
            )
        )

        bid = float(
            ticker.get(
                "bidPrice",
                0
            )
        )

        ask = float(
            ticker.get(
                "askPrice",
                0
            )
        )

        change = float(
            ticker.get(
                "priceChangePercent",
                0
            )
        )

        volatility = 0.0

        if last_price > 0:
            volatility = (
                abs(high - low)
                /
                last_price
                *
                100
            )

        liquidity_score = volume

        alpha_score = (
            volatility
            *
            volume
        )

        tradefi_score = (
            abs(change)
            *
            volume
        )

        return SymbolState(
            symbol=ticker["symbol"],
            exchange="BINANCE",
            last_price=last_price,
            bid_price=bid,
            ask_price=ask,
            volume=volume,
            alpha_score=alpha_score,
            tradefi_score=tradefi_score,
            volatility=volatility,
            liquidity_score=liquidity_score,
            price_change_percent=change,
            timestamp=datetime.now(
                timezone.utc
            ),
            market_status="ACTIVE"
        )


    def _validate_response(
        self,
        response: Dict[str, Any]
    ):
        """
        Validate HTTP response contract.
        """

        if response.get("status") != 200:
            raise ValueError(
                "Invalid Binance response status"
            )

        if "body" not in response:
            raise ValueError(
                "Missing response body"
            )
