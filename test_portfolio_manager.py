from brain.portfolio_manager import PortfolioManager


def run_portfolio_manager_test():

    print(
        "========== PORTFOLIO MANAGER TEST =========="
    )


    manager = PortfolioManager(
        max_positions=5,
        max_exposure=0.50
    )


    balance = 1000


    # Existing positions simulation

    positions = {

        "BTCUSDT": [
            {
                "size": 100
            }
        ],

        "ETHUSDT": [
            {
                "size": 50
            }
        ]

    }


    # =========================
    # TEST 1: Exposure
    # =========================

    exposure = manager.total_exposure(
        positions
    )

    print(
        "\nTOTAL EXPOSURE:",
        exposure
    )

    assert exposure == 150



    # =========================
    # TEST 2: Position Count
    # =========================

    count = manager.position_count(
        positions
    )

    print(
        "POSITION COUNT:",
        count
    )

    assert count == 2



    # =========================
    # TEST 3: SAFE NEW POSITION
    # =========================

    result = manager.approve_new_position(
        balance,
        positions,
        new_size=100
    )

    print(
        "\nSAFE POSITION:",
        result
    )

    assert result == "APPROVED"



    # =========================
    # TEST 4: HIGH EXPOSURE BLOCK
    # =========================

    result = manager.approve_new_position(
        balance,
        positions,
        new_size=400
    )


    print(
        "HIGH EXPOSURE:",
        result
    )


    assert result == "BLOCKED"



    # =========================
    # TEST 5: Position Limit
    # =========================

    full_positions = {

        "A":[{"size":10}],
        "B":[{"size":10}],
        "C":[{"size":10}],
        "D":[{"size":10}],
        "E":[{"size":10}]
    }


    result = manager.approve_new_position(
        balance,
        full_positions,
        new_size=10
    )


    print(
        "MAX POSITIONS:",
        result
    )


    assert result == "BLOCKED"



    print(
        "\nPORTFOLIO MANAGER TEST PASSED ✅"
    )


if __name__ == "__main__":
    run_portfolio_manager_test()
