from parsers.binance_exchange_parser import BinanceExchangeParser
from registry.symbol_registry import SymbolRegistry
from adapters.binance_market_adapter import BinanceMarketAdapter
from market.market_manager import MarketManager
from models.symbol_state import SymbolState


def test_exchange_to_market_manager_pipeline():

    # Parser layer
    parser = BinanceExchangeParser()

    parsed_symbols = parser.parse(
        {
            "symbols": [
                {
                    "symbol": "PIPELINE_SYMBOL",
                    "status": "TRADING",
                    "baseAsset": "BASE",
                    "quoteAsset": "QUOTE",
                }
            ]
        }
    )

    # Registry layer
    registry = SymbolRegistry()

    registry.load_symbols(
        parsed_symbols
    )

    # Adapter layer
    adapter = BinanceMarketAdapter(
        registry
    )

    available = adapter.get_available_symbols()

    assert len(available) == 1


    # Domain state layer - Production contract integration fixed here
    symbol_state = SymbolState(
        exchange="BINANCE",
        symbol="PIPELINE_SYMBOL"
    )


    # Market manager layer
    manager = MarketManager()

    manager.activate_symbol(
        symbol_state
    )


    result = manager.get_market_state(
        "PIPELINE_SYMBOL"
    )


    assert result.symbol == "PIPELINE_SYMBOL"
