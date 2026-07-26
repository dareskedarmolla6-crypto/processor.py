from brain.execution_engine import ExecutionEngine
from brain.execution_persistence import ExecutionPersistence


def run_test():

    print(
        "========== EXECUTION LIFECYCLE TEST =========="
    )


    persistence = ExecutionPersistence(
        "test_execution.db"
    )


    engine = ExecutionEngine(
        persistence
    )


    # 1. OPEN
    position = engine.open(
        "BTCUSDT",
        "LONG",
        1.0,
        100
    )


    assert position["status"] == "OPEN"

    print(
        "✅ OPEN POSITION PASSED"
    )


    # 2. PARTIAL CLOSE

    partial = engine.partial_close_by_id(
        "BTCUSDT",
        position["id"],
        0.5,
        110
    )


    assert partial["remaining_size"] == 0.5


    print(
        "✅ PARTIAL CLOSE PASSED"
    )


    # 3. FULL CLOSE

    closed = engine.close_by_id(
        "BTCUSDT",
        position["id"],
        120,
        "TARGET"
    )


    assert closed["status"] == "CLOSED"


    print(
        "✅ FULL CLOSE PASSED"
    )


    # 4. RESTORE

    restored = persistence.restore_positions()


    assert isinstance(
        restored,
        list
    )


    print(
        "✅ RESTORE PASSED"
    )


    print(
        "\n✅ EXECUTION LIFECYCLE TEST PASSED"
    )


if __name__ == "__main__":
    run_test()
