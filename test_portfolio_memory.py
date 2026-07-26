from brain.portfolio_memory import PortfolioMemory


def run_test():

    print("========== PORTFOLIO MEMORY V7.5 ==========")


    memory = PortfolioMemory()


    allocations = [

        {
            "symbol": "BTCUSDT",
            "allocation": 450,
            "action": "INCREASE"
        },

        {
            "symbol": "SOLUSDT",
            "allocation": 450,
            "action": "INCREASE"
        },

        {
            "symbol": "ETHUSDT",
            "allocation": 100,
            "action": "REDUCE"
        }

    ]


    result = memory.update(
        allocations
    )


    print("\nPORTFOLIO:")
    print(result)


    print("\nHISTORY:")
    print(memory.get_history())


    btc = memory.get_allocation(
        "BTCUSDT"
    )

    print("\nBTC:")
    print(btc)


    print(
        "\nPORTFOLIO MEMORY V7.5 PASSED ✅"
    )


if __name__ == "__main__":
    run_test()
