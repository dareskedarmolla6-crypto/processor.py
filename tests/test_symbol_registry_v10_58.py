from registry.symbol_registry import SymbolRegistry


def test_symbol_registry_loads_parser_output():

    registry = SymbolRegistry()

    parsed_symbols = [
        {
            "symbol": "TEST_SYMBOL",
            "status": "TRADING",
            "base_asset": "BASE",
            "quote_asset": "QUOTE",
        }
    ]

    registry.load_symbols(parsed_symbols)

    assert registry.count() == 1

    result = registry.get_symbol(
        "TEST_SYMBOL"
    )

    assert result["status"] == "TRADING"


def test_symbol_registry_filters_trading_symbols():

    registry = SymbolRegistry()

    registry.load_symbols(
        [
            {
                "symbol": "ACTIVE",
                "status": "TRADING",
            },
            {
                "symbol": "INACTIVE",
                "status": "BREAK",
            },
        ]
    )

    trading = registry.get_trading_symbols()

    assert len(trading) == 1
