from datetime import datetime, timezone

from models.symbol_state import SymbolState


class MarketValidator:
    """
    Production market data validation layer.

    Validates incoming market states before
    they enter the internal market pipeline.
    """

    def validate(self, state: SymbolState) -> bool:
        """
        Validate complete market state.
        """

        self._validate_symbol(state.symbol)
        self._validate_price(state.last_price)
        self._validate_timestamp(state.timestamp)

        return True

    def _validate_symbol(self, symbol: str) -> None:
        if not symbol:
            raise ValueError("Symbol cannot be empty")

        if not isinstance(symbol, str):
            raise TypeError("Symbol must be string")

    def _validate_price(self, price: float) -> None:
        if price is None:
            raise ValueError("Price cannot be None")

        if price <= 0:
            raise ValueError(
                "Price must be greater than zero"
            )

    def _validate_timestamp(
        self,
        timestamp: datetime
    ) -> None:

        if timestamp is None:
            raise ValueError(
                "Timestamp cannot be None"
            )

        if timestamp.tzinfo is None:
            raise ValueError(
                "Timestamp must contain timezone"
            )

        now = datetime.now(timezone.utc)

        if timestamp > now:
            raise ValueError(
                "Timestamp cannot be in future"
            )
