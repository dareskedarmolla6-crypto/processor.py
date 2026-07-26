from parsers.binance_exchange_parser import BinanceExchangeParser


def test_exchange_parser_extracts_symbols():
    parser = BinanceExchangeParser()

    exchange_response = {
        "symbols": [
            {
                "symbol": "REAL_SYMBOL_FROM_RESPONSE",
                "status": "TRADING",
                "baseAsset": "BASE",
                "quoteAsset": "QUOTE",
            }
        ]
    }

    result = parser.parse(exchange_response)

    assert len(result) == 1

    assert result[0]["symbol"] == "REAL_SYMBOL_FROM_RESPONSE"
    assert result[0]["status"] == "TRADING"
    assert result[0]["base_asset"] == "BASE"
    assert result[0]["quote_asset"] == "QUOTE"


def test_exchange_parser_rejects_invalid_response():
    parser = BinanceExchangeParser()

    invalid_response = {}

    try:
        parser.parse(invalid_response)
        assert False
    except ValueError:
        assert True
