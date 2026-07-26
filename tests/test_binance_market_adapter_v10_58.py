from adapters.binance_market_adapter import BinanceMarketAdapter
from registry.symbol_registry import SymbolRegistry


def test_market_adapter_returns_trading_symbols():

    registry = SymbolRegistry()

    registry.load_symbols(
        [
            {
                "symbol": "ACTIVE_SYMBOL",
                "status": "TRADING",
            },
            {
                "symbol": "STOPPED_SYMBOL",
                "status": "BREAK",
            },
        ]
    )

    adapter = BinanceMarketAdapter(
        registry
    )

    symbols = adapter.get_available_symbols()

    assert len(symbols) == 1
    assert symbols[0]["symbol"] == "ACTIVE_SYMBOL"


def test_market_adapter_symbol_lookup():

    registry = SymbolRegistry()

    registry.load_symbols(
        [
            {
                "symbol": "LOOKUP_SYMBOL",
                "status": "TRADING",
            }
        ]
    )

    adapter = BinanceMarketAdapter(
        registry
    )

    result = adapter.get_symbol(
        "LOOKUP_SYMBOL"
    )

    assert result["status"] == "TRADING"
