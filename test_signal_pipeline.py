from brain.performance_memory import PerformanceMemory
from brain.signal_pipeline import SignalPipeline

def run_signal_pipeline_test():

    print("========== SIGNAL PIPELINE TEST ==========")

    memory = PerformanceMemory()

    # Performance History
    # BTC: 2 Wins, 0 Losses -> Confidence Boost
    memory.record("BTCUSDT", 100)
    memory.record("BTCUSDT", 50)

    # ETH: 0 Wins, 2 Losses -> Confidence Penalty
    memory.record("ETHUSDT", -20)
    memory.record("ETHUSDT", -30)

    pipeline = SignalPipeline(memory)

    market = [
        {"symbol": "BTCUSDT", "price": 60000, "signal": "BUY", "confidence": 0.75},
        {"symbol": "ETHUSDT", "price": 3000, "signal": "BUY", "confidence": 0.75},
        {"symbol": "SOLUSDT", "price": 150, "signal": "SELL", "confidence": 0.80}
    ]

    results = pipeline.process(market)

    print("\nPIPELINE RESULTS:\n")
    for r in results:
        print(r)

    # ውጤቶችን ማግኘት
    btc = next(x for x in results if x["symbol"] == "BTCUSDT")
    eth = next(x for x in results if x["symbol"] == "ETHUSDT")
    sol = next(x for x in results if x["symbol"] == "SOLUSDT")

    # ማረጋገጫ (Assertions)
    assert btc["decision"] == "TRADE"
    assert eth["decision"] == "SKIP"
    assert sol["decision"] == "SKIP" # አሁን SOL ከ 0.75 በታች ስለሆነ SKIP ይሆናል

    print("\nSIGNAL PIPELINE TEST PASSED ✅")

if __name__ == "__main__":
    run_signal_pipeline_test()
