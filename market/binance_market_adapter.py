from models.symbol_state import SymbolState


class BinanceMarketAdapter:
    """
    Converts validated Binance responses into SymbolState.

    Responsibilities:
        - Convert Binance market responses
        - Calculate market classification metrics
        - Create validated SymbolState

    Does NOT contain:
        - Trading execution
        - Strategy decisions
        - Risk decisions
    """

    EXCHANGE_NAME = "BINANCE"


    def from_ticker(
        self,
        ticker: dict
    ) -> SymbolState:

        return SymbolState(
            symbol=ticker["symbol"],
            exchange=self.EXCHANGE_NAME,
            last_price=float(
                ticker["price"]
            )
        )


    def from_24h(
        self,
        ticker: dict
    ) -> SymbolState:

        last_price = float(
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


        price_change_raw = ticker.get(
            "priceChangePercent"
        )

        if price_change_raw is None:
            price_change = 0.0
        else:
            price_change = float(price_change_raw)


        tradefi_score = (
            abs(price_change)
            *
            volume
        )


        return SymbolState(
            symbol=ticker["symbol"],
            exchange=self.EXCHANGE_NAME,

            last_price=last_price,

            bid_price=float(
                ticker.get(
                    "bidPrice",
                    0
                )
            ),

            ask_price=float(
                ticker.get(
                    "askPrice",
                    0
                )
            ),

            volume=volume,

            alpha_score=alpha_score,

            tradefi_score=tradefi_score,

            volatility=volatility,

            liquidity_score=liquidity_score,

            price_change_percent=price_change,

            market_status="ACTIVE"
        )
