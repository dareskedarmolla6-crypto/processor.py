from typing import List


class SymbolActivationPolicy:
    """
    Production symbol activation policy.

    Responsibilities:
    - Select exchange-valid symbols
    - Remove unsupported assets
    - Enforce activation universe boundary

    Does NOT contain:
    - Market data fetching
    - Trading decisions
    - Strategy logic
    - Risk logic
    """

    MAX_SYMBOLS = 20

    BLOCKED_BASE_ASSETS = {
        "USDC",
        "FDUSD",
        "TUSD",
        "EUR",
        "AEUR"
    }

    def __init__(
        self,
        quote_asset: str = "USDT"
    ):
        self.quote_asset = quote_asset


    def filter(
        self,
        symbols: List[dict]
    ) -> List[str]:

        if not symbols:
            raise ValueError(
                "Symbols cannot be empty"
            )

        valid = [
            symbol["symbol"]
            for symbol in symbols
            if self._is_valid(symbol)
        ]

        return valid[:self.MAX_SYMBOLS]


    def _is_valid(
        self,
        symbol: dict
    ) -> bool:

        name = symbol.get("symbol")
        base = symbol.get("base_asset")

        if base is None and isinstance(name, str):
            base = name.replace(
                self.quote_asset,
                ""
            )

        return (
            symbol.get("status") == "TRADING"
            and
            symbol.get("quote_asset") == self.quote_asset
            and
            isinstance(name, str)
            and
            name.isascii()
            and
            isinstance(base, str)
            and
            base.isascii()
            and
            base not in self.BLOCKED_BASE_ASSETS
        )
