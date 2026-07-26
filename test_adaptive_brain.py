from brain.performance_memory import PerformanceMemory
from brain.adaptive_brain import AdaptiveBrain


def run_test():

    print("========== ADAPTIVE BRAIN TEST ==========")

    memory = PerformanceMemory()

    # የቀድሞ ውጤቶች
    memory.record("BTCUSDT", 50)
    memory.record("BTCUSDT", 40)
    memory.record("ETHUSDT", -20)
    memory.record("ETHUSDT", -30)

    brain = AdaptiveBrain(memory)

    btc = brain.evaluate({
        "symbol": "BTCUSDT",
        "signal": "BUY",
        "confidence": 0.70
    })

    eth = brain.evaluate({
        "symbol": "ETHUSDT",
        "signal": "BUY",
        "confidence": 0.70
    })

    print("\nBTC RESULT:")
    print(btc)

    print("\nETH RESULT:")
    print(eth)

    assert btc["decision"] == "TRADE"
    assert eth["decision"] == "SKIP"

    print("\nADAPTIVE BRAIN TEST PASSED ✅")


if __name__ == "__main__":
    run_test()
