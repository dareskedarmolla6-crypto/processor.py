from brain.performance_memory import PerformanceMemory
from brain.reward_engine import RewardEngine


def run_test():

    print("========== REWARD ENGINE TEST ==========")


    memory = PerformanceMemory()

    reward = RewardEngine(
        memory
    )


    # WIN TEST
    btc = reward.evaluate(
        "BTCUSDT",
        100
    )

    print("\nBTC:")
    print(btc)



    # LOSS TEST
    eth = reward.evaluate(
        "ETHUSDT",
        -50
    )

    print("\nETH:")
    print(eth)



    # BATCH TEST
    batch = reward.process_batch(
        [
            {
                "symbol":"SOLUSDT",
                "pnl":80
            },
            {
                "symbol":"BNBUSDT",
                "pnl":-30
            }
        ]
    )


    print("\nBATCH:")
    print(batch)


    print("\nMEMORY:")
    print(memory.history)


    assert btc["status"] == "WIN"
    assert eth["status"] == "LOSS"
    assert len(batch) == 2


    print("\nREWARD ENGINE TEST PASSED ✅")


if __name__ == "__main__":
    run_test()
