from brain.execution_engine import ExecutionEngine


def run_metadata_test():
    print("========== EXECUTION METADATA TEST ==========")

    execution = ExecutionEngine()

    # 1. OPEN POSITION
    position = execution.open(
        "COIN_C",
        "LONG",
        30.0,
        50
    )

    print("OPEN:", position)

    assert position["status"] == "OPEN"
    assert position["highest_price"] == 50
    assert position["locked_profit"] == 0


    # 2. UPDATE METADATA (LOCK PROFIT)
    updated = execution.update_position_meta(
        "COIN_C",
        position["id"],
        {
            "locked_profit": 10.0,
            "trailing_price": 55
        }
    )

    print("UPDATED:", updated)


    # 3. VERIFY METADATA
    assert updated["locked_profit"] == 10.0
    assert updated["trailing_price"] == 55

    print("\nMetadata Update Passed ✅")


if __name__ == "__main__":
    run_metadata_test()
