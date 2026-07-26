from market.symbol_activation_policy import (
    SymbolActivationPolicy
)


def test_activation_policy_filters_symbols():

    policy = SymbolActivationPolicy(
        quote_asset="USDT"
    )


    symbols = [
        {
            "symbol": "BTCUSDT",
            "status": "TRADING",
            "quote_asset": "USDT"
        },
        {
            "symbol": "ETHBTC",
            "status": "TRADING",
            "quote_asset": "BTC"
        },
        {
            "symbol": "BNBUSDT",
            "status": "BREAK",
            "quote_asset": "USDT"
        }
    ]


    result = policy.filter(
        symbols
    )


    assert result == [
        "BTCUSDT"
    ]



def test_activation_policy_requires_symbols():

    policy = SymbolActivationPolicy()


    try:
        policy.filter([])

        assert False

    except ValueError:
        assert True
