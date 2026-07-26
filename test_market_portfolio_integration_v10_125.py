from models.symbol_state import SymbolState
from brain.market_portfolio_integration import MarketPortfolioIntegration


class StubPortfolioBrain:

    def __init__(self):
        self.received = None


    def rebalance(self, portfolio):

        self.received = portfolio

        return [
            {
                "symbol": "BTCUSDT",
                "rating": "STRONG",
                "new_allocation": 525
            }
        ]



def test_market_state_reaches_portfolio_intelligence():

    brain = StubPortfolioBrain()

    integration = MarketPortfolioIntegration(
        brain
    )


    state = SymbolState(
        symbol="BTCUSDT",
        exchange="BINANCE",
        last_price=60000.0,
        bid_price=59999.0,
        ask_price=60001.0,
        volume=2500.0,
        market_status="ACTIVE"
    )


    portfolio = [
        {
            "symbol": "BTCUSDT",
            "allocation": 500
        }
    ]


    result = integration.process(
        state,
        portfolio
    )


    assert result[0]["rating"] == "STRONG"

    assert brain.received[0]["symbol"] == "BTCUSDT"



def test_market_portfolio_rejects_invalid_state():

    brain = StubPortfolioBrain()

    integration = MarketPortfolioIntegration(
        brain
    )


    try:

        integration.process(
            None,
            []
        )

        assert False

    except ValueError:

        assert True
