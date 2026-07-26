from models.symbol_state import SymbolState


class BinanceMarketAdapter:
    """
    Converts validated Binance responses into SymbolState.

    Responsibilities:
        - Convert Binance response format
        - Create validated SymbolState

    Does NOT contain:
        - HTTP requests
        - Trading logic
        - Strategy logic
        - Risk logic
    """

    EXCHANGE_NAME = "BINANCE"

    def from_ticker(self, ticker: dict) -> SymbolState:

        return SymbolState(
            symbol=ticker["symbol"],
            exchange=self.EXCHANGE_NAME,
            last_price=float(ticker["price"])
        )


    def from_24h(self, ticker: dict) -> SymbolState:

        return SymbolState(
            symbol=ticker["symbol"],
            exchange=self.EXCHANGE_NAME,
            last_price=float(ticker["lastPrice"]),
            bid_price=float(ticker["bidPrice"]),
            ask_price=float(ticker["askPrice"]),
            volume=float(ticker["volume"]),
            market_status="ACTIVE"
        )
