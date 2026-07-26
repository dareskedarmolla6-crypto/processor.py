class AutonomousMarketDecisionService:
    """
    Coordinates the complete market intelligence decision flow.

    SymbolState
        ↓
    MarketIntelligenceBridge
        ↓
    MarketPortfolioIntegration
        ↓
    Portfolio Decision
    """

    def __init__(
        self,
        bridge,
        portfolio_integration
    ):
        self._bridge = bridge
        self._portfolio_integration = portfolio_integration

    def evaluate(
        self,
        state,
        portfolio
    ):
        if state is None:
            raise ValueError("state is required")

        if portfolio is None:
            raise ValueError("portfolio is required")

        market_input = self._bridge.convert(
            state
        )

        return self._portfolio_integration.process(
            market_input,
            portfolio
        )
