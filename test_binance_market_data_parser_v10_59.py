import json
from parsers.binance_market_data_parser import BinanceMarketDataParser

def test_parse_ticker_price_valid():
    parser = BinanceMarketDataParser()
    
    # እውነተኛ የፓርሰር ኮንትራትን የሚከተል የቢናንስ ሪስፖንስ ውቅር
    response = {
        "status": 200,
        "body": json.dumps({
            "symbol": "BTCUSDT",
            "price": "123.45"
        })
    }
    
    state = parser.parse_ticker_price(response)
    
    # የአሰርሽን ማስተካከያ (state.price ወደ state.last_price ተቀይሯል)
    assert state.symbol == "BTCUSDT"
    assert state.last_price == 123.45

if __name__ == "__main__":
    test_parse_ticker_price_valid()
    print("BinanceMarketDataParser tests PASSED ✅")
