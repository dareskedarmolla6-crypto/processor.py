from market.market_feed_service import MarketFeedService
from models.symbol_state import SymbolState


class StubMarketClient:
    """
    Isolated dependency contract test.
    """

    def get_ticker_price(self, symbol):

        return {
            "status": 200,
            "body": (
                '{"symbol":"'
                + symbol
                + '","price":"100.50"}'
            ).encode()
        }



class StubParser:

    def parse_ticker_price(self, response):

        return SymbolState(
            exchange="BINANCE",
            symbol="BTCUSDT",
            last_price=100.50
        )



class StubPipeline:

    def __init__(self):
        self.state = None

    def process(self, state):

        self.state = state



def test_market_feed_updates_pipeline():

    pipeline = StubPipeline()

    service = MarketFeedService(
        market_client=StubMarketClient(),
        parser=StubParser(),
        pipeline=pipeline
    )


    service.update_symbol(
        "BTCUSDT"
    )


    assert pipeline.state.symbol == "BTCUSDT"
    assert pipeline.state.last_price == 100.50
