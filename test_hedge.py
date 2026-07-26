from brain.execution_engine import ExecutionEngine
from brain.hedge_engine import HedgeEngine


def test():

    execution = ExecutionEngine()

    hedge = HedgeEngine(execution)

    symbol = "TESTCOIN"
    price = 100

    print("--- OPEN ORIGINAL LONG ---")

    execution.open(
        symbol,
        "LONG",
        1,
        price
    )

    print(execution.positions)


    print("\n--- CHECK HEDGE CONDITION ---")

    market = {
        "volatility": 30
    }

    if hedge.should_hedge(market):

        hedge.apply_hedge(
            symbol,
            price,
            "LONG"
        )


    print("\n--- FINAL POSITIONS ---")
    print(execution.positions)


if __name__ == "__main__":
    test()
