from typing import List
import json

from market.market_manager import MarketManager
from clients.binance_market_data_client import BinanceMarketDataClient
from parsers.binance_market_data_parser import BinanceMarketDataParser
from registry.symbol_registry import SymbolRegistry


class MarketSymbolActivator:
    """
    Production symbol activation service.

    Responsibilities:
        - Rank discovered symbols by real market quality
        - Activate selected market symbols
        - Load initial validated market state

    Does NOT contain:
        - Trading logic
        - Strategy logic
        - Risk logic
    """

    MAX_ACTIVE_SYMBOLS = 20

    def __init__(
        self,
        registry: SymbolRegistry,
        market_client: BinanceMarketDataClient,
        parser: BinanceMarketDataParser,
        manager: MarketManager
    ):
        self.registry = registry
        self.market_client = market_client
        self.parser = parser
        self.manager = manager

    def activate(
        self,
        symbols: List[str]
    ) -> None:

        if not symbols:
            raise ValueError(
                "Symbols cannot be empty"
            )

        ticker_response = (
            self.market_client
            .get_all_ticker_24h()
        )

        ticker_data = self._decode_response(
            ticker_response
        )

        quality_symbols = (
            self._rank_quality_symbols(
                symbols,
                ticker_data
            )
        )

        selected_symbols = quality_symbols[
            :self.MAX_ACTIVE_SYMBOLS
        ]

        for symbol in selected_symbols:
            try:
                ticker = self._find_ticker(
                    symbol,
                    ticker_data
                )

                state = self.parser.parse_ticker_24h(
                    ticker
                )

                self.manager.activate_symbol(
                    state
                )

            except Exception:
                continue

    def _rank_quality_symbols(
        self,
        symbols: List[str],
        ticker_data: List[dict]
    ) -> List[str]:

        ticker_map = {
            item.get("symbol"): item
            for item in ticker_data
        }

        ranked = []

        for symbol in symbols:

            ticker = ticker_map.get(
                symbol
            )

            if not ticker:
                continue

            try:
                price = float(
                    ticker.get(
                        "lastPrice",
                        0
                    )
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

                if price <= 0 or volume <= 0:
                    continue

                if price < 0.00012 or price > 0.01:
                    continue

                volatility = (
                    abs(high - low)
                    /
                    price
                    *
                    100
                )

                score = (
                    volatility *
                    volume
                )

                ranked.append(
                    (
                        symbol,
                        score
                    )
                )

            except Exception:
                continue

        ranked.sort(
            key=lambda item: item[1],
            reverse=True
        )

        return [
            item[0]
            for item in ranked
        ]

    def _decode_response(
        self,
        response: dict
    ) -> List[dict]:

        body = response.get(
            "body"
        )

        if isinstance(body, bytes):
            body = body.decode(
                "utf-8"
            )

        return json.loads(
            body
        )

    def _find_ticker(
        self,
        symbol: str,
        ticker_data: List[dict]
    ) -> dict:

        for item in ticker_data:

            if item.get("symbol") == symbol:
                return item

        raise ValueError(
            f"Ticker not found: {symbol}"
        )
