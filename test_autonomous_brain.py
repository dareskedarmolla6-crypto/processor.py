from brain.performance_memory import PerformanceMemory
from brain.autonomous_brain import AutonomousBrain


def run_test():

    print("========== AUTONOMOUS BRAIN TEST ==========")


    memory = PerformanceMemory()


    # Learning history

    memory.record(
        "BTCUSDT",
        100
    )

    memory.record(
        "BTCUSDT",
        50
    )


    memory.record(
        "ETHUSDT",
        -50
    )



    brain = AutonomousBrain(
        memory
    )


    signals = [

        {
            "symbol":"BTCUSDT",
            "signal":"BUY",
            "confidence":0.75
        },

        {
            "symbol":"ETHUSDT",
            "signal":"BUY",
            "confidence":0.75
        }

    ]



    result = brain.run_cycle(
        signals
    )


    print("\nRESULT:")
    print(result)



    assert len(
        result["decisions"]
    ) == 2


    assert (
        result["learning"]
        ["confidence_threshold"]
        == 0.70
    )


    print(
        "\nAUTONOMOUS BRAIN TEST PASSED ✅"
    )



if __name__ == "__main__":
    run_test()
