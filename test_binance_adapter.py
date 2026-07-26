from adapters.binance_adapter import BinanceMarketAdapter
from adapters.market_data_adapter import MarketDataAdapter


def test_binance_adapter_inherits_contract():
    adapter = BinanceMarketAdapter()

    assert isinstance(
        adapter,
        MarketDataAdapter
    )


def test_binance_adapter_methods_exist():
    adapter = BinanceMarketAdapter()

    assert hasattr(adapter, "connect")
    assert hasattr(adapter, "get_symbols")
    assert hasattr(adapter, "get_market_state")
    assert hasattr(adapter, "close")


def test_not_implemented_without_real_connection():
    adapter = BinanceMarketAdapter()

    try:
        adapter.get_symbols()
        assert False
    except NotImplementedError:
        assert True


if __name__ == "__main__":
    test_binance_adapter_inherits_contract()
    test_binance_adapter_methods_exist()
    test_not_implemented_without_real_connection()

    print("BinanceAdapter tests PASSED ✅")
