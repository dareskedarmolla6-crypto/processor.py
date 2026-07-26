from typing import Any


class BinanceExchangeParser:
    """
    Production parser for Binance exchangeInfo response.

    Responsibility:
    - Validate Binance API response
    - Extract exchange symbols
    - Convert external format into FSE internal format

    Not responsible for:
    - Trading decisions
    - Market analysis
    - Order execution
    """

    REQUIRED_FIELDS = {
        "symbol",
        "status",
        "baseAsset",
        "quoteAsset",
    }

    def parse(self, response: dict[str, Any]) -> list[dict[str, str]]:
        self._validate_response(response)

        symbols = response.get("symbols", [])

        return [
            self._parse_symbol(symbol)
            for symbol in symbols
            if self._is_valid_symbol(symbol)
        ]

    def _validate_response(self, response: dict[str, Any]) -> None:
        if not isinstance(response, dict):
            raise ValueError(
                "exchangeInfo response must be dictionary"
            )

        if "symbols" not in response:
            raise ValueError(
                "exchangeInfo response missing symbols"
            )

    def _is_valid_symbol(self, symbol: dict[str, Any]) -> bool:
        if not isinstance(symbol, dict):
            return False

        return self.REQUIRED_FIELDS.issubset(
            symbol.keys()
        )

    def _parse_symbol(
        self,
        symbol: dict[str, Any]
    ) -> dict[str, str]:

        return {
            "symbol": symbol["symbol"],
            "status": symbol["status"],
            "base_asset": symbol["baseAsset"],
            "quote_asset": symbol["quoteAsset"],
        }
