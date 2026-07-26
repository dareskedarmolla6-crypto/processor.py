from brain.performance_memory import PerformanceMemory
from brain.reward_engine import RewardEngine
from brain.self_optimizer import SelfOptimizer
from brain.feedback_loop import FeedbackLoop



def run_test():

    print("========== FEEDBACK LOOP TEST ==========")


    memory = PerformanceMemory()


    reward = RewardEngine(
        memory
    )


    optimizer = SelfOptimizer(
        memory
    )


    feedback = FeedbackLoop(

        reward_engine=reward,

        performance_memory=memory,

        optimizer=optimizer

    )


    # -------------------------
    # SINGLE RESULTS
    # -------------------------

    btc = feedback.process_trade_result(
        "BTCUSDT",
        100
    )


    eth = feedback.process_trade_result(
        "ETHUSDT",
        -50
    )


    print("\nBTC:")
    print(btc)


    print("\nETH:")
    print(eth)



    # -------------------------
    # BATCH RESULTS
    # -------------------------

    batch = feedback.process_batch(

        [

            {
                "symbol": "SOLUSDT",
                "pnl": 80
            },

            {
                "symbol": "BNBUSDT",
                "pnl": -30
            }

        ]

    )


    print("\nBATCH:")
    print(batch)



    # -------------------------
    # MEMORY
    # -------------------------

    print("\nMEMORY:")
    print(memory.history)



    # -------------------------
    # LEARNING
    # -------------------------

    learning = feedback.learn()


    print("\nLEARNING:")
    print(learning)



    assert memory.history["BTCUSDT"]["wins"] == 1

    assert memory.history["ETHUSDT"]["losses"] == 1


    print(
        "\nFEEDBACK LOOP TEST PASSED ✅"
    )



if __name__ == "__main__":
    run_test()
