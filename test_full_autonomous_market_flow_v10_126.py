from models.symbol_state import SymbolState

from brain.market_intelligence_bridge import MarketIntelligenceBridge
from brain.market_portfolio_integration import MarketPortfolioIntegration


class StubPortfolioBrain:

    def rebalance(self, portfolio):

        return [
            {
                "symbol": portfolio[0]["symbol"],
                "rating": "STRONG",
                "new_allocation": 525
            }
        ]



class PortfolioAdapter:

    def __init__(self):

        self.received = None


    def analyze(self, market_input):

        self.received = market_input

        return {
            "symbol": market_input["symbol"],
            "allocation": 500
        }



def test_full_autonomous_market_flow():

    portfolio_brain = StubPortfolioBrain()


    integration = MarketPortfolioIntegration(
        portfolio_brain
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


    assert result[0]["symbol"] == "BTCUSDT"

    assert result[0]["rating"] == "STRONG"




def test_market_flow_rejects_empty_state():

    portfolio_brain = StubPortfolioBrain()

    integration = MarketPortfolioIntegration(
        portfolio_brain
    )


    try:

        integration.process(
            None,
            []
        )

        assert False

    except ValueError:

        assert True
