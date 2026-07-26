from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass(frozen=True)
class SymbolState:
    """
    Immutable market symbol state snapshot.

    Stores validated market data
    received from real market sources.

    No trading logic.
    No strategy logic.
    No risk logic.
    """

    symbol: str
    exchange: str

    last_price: Optional[float] = None

    bid_price: Optional[float] = None
    ask_price: Optional[float] = None

    volume: Optional[float] = None

    # Market classification metrics
    alpha_score: Optional[float] = None
    tradefi_score: Optional[float] = None
    volatility: Optional[float] = None
    liquidity_score: Optional[float] = None
    price_change_percent: Optional[float] = None

    timestamp: datetime = datetime.now(
        timezone.utc
    )

    market_status: str = "UNKNOWN"


    def __post_init__(self):
        self._validate()


    def _validate(self):

        if not self.symbol:
            raise ValueError(
                "Symbol cannot be empty"
            )


        if not self.exchange:
            raise ValueError(
                "Exchange cannot be empty"
            )


        if self.last_price is not None:
            if self.last_price <= 0:
                raise ValueError(
                    "Last price must be positive"
                )


        if self.bid_price is not None:
            if self.bid_price <= 0:
                raise ValueError(
                    "Bid price must be positive"
                )


        if self.ask_price is not None:
            if self.ask_price <= 0:
                raise ValueError(
                    "Ask price must be positive"
                )


        if (
            self.bid_price is not None
            and self.ask_price is not None
        ):
            if self.bid_price > self.ask_price:
                raise ValueError(
                    "Bid cannot exceed ask"
                )


        if self.volume is not None:
            if self.volume < 0:
                raise ValueError(
                    "Volume cannot be negative"
                )


        if self.volatility is not None:
            if self.volatility < 0:
                raise ValueError(
                    "Volatility cannot be negative"
                )


        if self.liquidity_score is not None:
            if self.liquidity_score < 0:
                raise ValueError(
                    "Liquidity score cannot be negative"
                )
