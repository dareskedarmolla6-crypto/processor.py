from models.symbol_state import SymbolState
from brain.market_intelligence_bridge import MarketIntelligenceBridge


class StubIntelligence:

    def __init__(self):
        self.received = None

    def analyze(self, market_input):

        self.received = market_input

        return {
            "decision": "HOLD",
            "symbol": market_input["symbol"]
        }


def test_bridge_converts_symbol_state():

    intelligence = StubIntelligence()

    bridge = MarketIntelligenceBridge(
        intelligence
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


    result = bridge.process(
        state
    )


    assert result["decision"] == "HOLD"

    assert intelligence.received["symbol"] == "BTCUSDT"

    assert intelligence.received["price"] == 60000.0



def test_bridge_rejects_invalid_state():

    intelligence = StubIntelligence()

    bridge = MarketIntelligenceBridge(
        intelligence
    )


    try:

        bridge.process(None)

        assert False

    except ValueError:

        assert True
