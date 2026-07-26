from brain.capital_allocator import CapitalAllocator


def run_capital_allocator_test():

    print("========== CAPITAL ALLOCATOR TEST ==========")

    allocator = CapitalAllocator(
        max_single_asset=0.20,
        max_total_exposure=0.50
    )

    balance = 1000


    # TEST 1: Risk Adjustment

    print("\nRISK ADJUSTMENT:")

    normal = allocator.adjust_risk(0, 0)
    win = allocator.adjust_risk(5, 0)
    loss = allocator.adjust_risk(0, 3)

    print("NORMAL:", normal)
    print("WIN:", win)
    print("LOSS:", loss)

    assert normal == 0.03
    assert win == 0.04
    assert loss == 0.01



    # TEST 2: Allocation

    opportunities = [
        {
            "symbol": "BTC",
            "confidence": 1.0
        },
        {
            "symbol": "ETH",
            "confidence": 0.5
        },
        {
            "symbol": "SOL",
            "confidence": 0.8
        }
    ]


    allocations = allocator.allocate(
        balance,
        opportunities
    )

    print("\nALLOCATIONS:")
    print(allocations)


    total = sum(allocations.values())

    print("TOTAL ALLOCATION:", total)


    assert total <= 500
    assert allocations["BTC"] <= 200



    # TEST 3: Exposure

    safe = allocator.check_exposure(
        balance,
        300
    )

    blocked = allocator.check_exposure(
        balance,
        500
    )


    print("\nSAFE EXPOSURE:", safe)
    print("BLOCKED EXPOSURE:", blocked)


    assert safe == "APPROVED"
    assert blocked == "BLOCKED"



    print("\nCAPITAL ALLOCATOR TEST PASSED ✅")



if __name__ == "__main__":
    run_capital_allocator_test()
