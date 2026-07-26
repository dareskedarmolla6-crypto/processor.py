from adapters.market_data_adapter import MarketDataAdapter


def test_adapter_is_abstract():
    try:
        MarketDataAdapter()
        assert False
    except TypeError:
        assert True


def test_adapter_contract_methods_exist():
    methods = [
        "connect",
        "get_symbols",
        "get_market_state",
        "close",
    ]

    for method in methods:
        assert hasattr(
            MarketDataAdapter,
            method
        )


if __name__ == "__main__":
    test_adapter_is_abstract()
    test_adapter_contract_methods_exist()

    print("MarketDataAdapter tests PASSED ✅")
