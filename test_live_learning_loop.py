from brain.performance_memory import PerformanceMemory
from brain.reward_engine import RewardEngine
from brain.self_optimizer import SelfOptimizer
from brain.feedback_loop import FeedbackLoop
from brain.live_learning_loop import LiveLearningLoop


class MockBrain:

    def process(self, signals):

        return [
            {
                "symbol": "BTCUSDT",
                "signal": "BUY",
                "confidence": 0.85,
                "decision": "TRADE"
            }
        ]



class MockExecution:

    def execute(self, decision):

        return {
            "action": "OPEN",
            "side": "LONG",
            "symbol": decision["symbol"]
        }



def run_test():

    print("========== LIVE LEARNING LOOP TEST ==========")


    memory = PerformanceMemory()


    reward = RewardEngine(
        memory
    )


    optimizer = SelfOptimizer(
        memory
    )


    feedback = FeedbackLoop(
        reward,
        memory,
        optimizer
    )


    brain = MockBrain()

    execution = MockExecution()



    live = LiveLearningLoop(
        brain,
        execution,
        feedback
    )


    signals = [
        {
            "symbol": "BTCUSDT",
            "price": 60000,
            "signal": "BUY",
            "confidence": 0.85
        }
    ]



    cycle = live.run(
        signals
    )


    print("\nLIVE CYCLE:")
    print(cycle)



    closed_trades = [

        {
            "symbol": "BTCUSDT",
            "pnl": 100
        }

    ]



    update = live.update_feedback(
        closed_trades
    )


    print("\nFEEDBACK UPDATE:")
    print(update)



    print("\nMEMORY:")
    print(memory.history)



    assert memory.history["BTCUSDT"]["wins"] == 1


    print(
        "\nLIVE LEARNING LOOP TEST PASSED ✅"
    )



if __name__ == "__main__":
    run_test()
