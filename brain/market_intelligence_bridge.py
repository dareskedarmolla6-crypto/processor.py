class MarketIntelligenceBridge:
    """
    Bridge between Market Data layer and Intelligence layer.

    SymbolState
        ↓
    Market Intelligence Input
        ↓
    Intelligence Engine
    """

    def __init__(
        self,
        intelligence
    ):
        self._intelligence = intelligence


    def process(
        self,
        state
    ):

        if state is None:
            raise ValueError(
                "SymbolState is required"
            )


        market_input = {
            "symbol": state.symbol,
            "price": state.last_price,
            "bid": state.bid_price,
            "ask": state.ask_price,
            "volume": state.volume,
            "exchange": state.exchange,
            "status": state.market_status
        }


        return self._intelligence.analyze(
            market_input
        )
