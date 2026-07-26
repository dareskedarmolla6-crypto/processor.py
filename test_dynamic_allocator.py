from brain.dynamic_allocator import DynamicAllocator


def run_test():

    print("========== DYNAMIC ALLOCATOR V7.5.1 ==========")


    allocator = DynamicAllocator()


    assets = [

        {
            "symbol": "BTCUSDT",
            "score": 100,
            "status": "STRONG"
        },

        {
            "symbol": "ETHUSDT",
            "score": 0,
            "status": "WEAK"
        },

        {
            "symbol": "SOLUSDT",
            "score": 100,
            "status": "STRONG"
        }

    ]


    result = allocator.allocate(
        1000,
        assets
    )


    print("\nALLOCATIONS:")
    print(result)


    print(
        "\nDYNAMIC ALLOCATOR V7.5.1 PASSED ✅"
    )


if __name__ == "__main__":
    run_test()
