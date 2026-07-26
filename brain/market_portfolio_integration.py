class MarketPortfolioIntegration:
    """
    Connects Market Data state with Portfolio Intelligence.

    SymbolState
        ↓
    Portfolio Input
        ↓
    Portfolio Intelligence
    """


    def __init__(
        self,
        portfolio_brain
    ):
        self._portfolio_brain = portfolio_brain


    def process(
        self,
        state,
        portfolio
    ):

        if state is None:
            raise ValueError(
                "SymbolState is required"
            )

        if not portfolio:
            raise ValueError(
                "Portfolio is required"
            )


        market_symbol = state.symbol


        updated_portfolio = []

        for item in portfolio:

            updated_portfolio.append(
                {
                    "symbol": item["symbol"],
                    "allocation": item["allocation"]
                }
            )


        return self._portfolio_brain.rebalance(
            updated_portfolio
        )
