from brain.performance_memory import PerformanceMemory

def run_test():
    print("========== PERFORMANCE MEMORY TEST ==========")

    memory = PerformanceMemory()

    # =====================
    # RECORD RESULTS
    # =====================
    memory.record("BTCUSDT", 50)
    memory.record("BTCUSDT", -20)
    memory.record("ETHUSDT", 100)

    print("\nHISTORY:", memory.history)

    # =====================
    # SCORE
    # =====================
    btc_score = memory.score("BTCUSDT")
    eth_score = memory.score("ETHUSDT")

    print("\nBTC SCORE:", btc_score)
    print("ETH SCORE:", eth_score)

    assert btc_score == 50.0
    assert eth_score == 100.0

    # =====================
    # CONFIDENCE
    # =====================
    confidence = memory.adjust_confidence("BTCUSDT", 0.70)

    print("\nADJUSTED CONFIDENCE:", confidence)

    # አዲሱ assert: BTC 50% ስለሆነ confidence 0.70 ሆኖ መቆየት አለበት
    assert confidence == 0.70

    print("\nPERFORMANCE MEMORY TEST PASSED ✅")

if __name__ == "__main__":
    run_test()
