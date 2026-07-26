from market.symbol_discovery_service import (
    SymbolDiscoveryService
)

from registry.symbol_registry import (
    SymbolRegistry
)

from parsers.binance_exchange_parser import (
    BinanceExchangeParser
)

from market.symbol_activation_policy import (
    SymbolActivationPolicy
)


class StubSymbolClient:

    def get_exchange_info(self):

        return {
            "symbols": [
                {
                    "symbol": "BTCUSDT",
                    "status": "TRADING",
                    "baseAsset": "BTC",
                    "quoteAsset": "USDT"
                },
                {
                    "symbol": "ETHUSDT",
                    "status": "TRADING",
                    "baseAsset": "ETH",
                    "quoteAsset": "USDT"
                }
            ]
        }



def test_symbol_discovery_loads_registry():

    registry = SymbolRegistry()

    service = SymbolDiscoveryService(
        StubSymbolClient(),
        BinanceExchangeParser(),
        registry,
        SymbolActivationPolicy()
    )

    service.discover()

    symbols = registry.get_trading_symbols()

    assert len(symbols) == 2
    assert symbols[0]["symbol"] == "BTCUSDT"



def test_symbol_discovery_empty_response_rejected():

    registry = SymbolRegistry()

    class EmptyClient:

        def get_exchange_info(self):
            return {}


    service = SymbolDiscoveryService(
        EmptyClient(),
        BinanceExchangeParser(),
        registry,
        SymbolActivationPolicy()
    )


    try:
        service.discover()
        assert False

    except ValueError:
        assert True
