from brain.portfolio_rebalancer import PortfolioRebalancer


def run_test():

    print(
        "========== PORTFOLIO REBALANCE V7.4 =========="
    )


    report = {

        "BTCUSDT": {
            "score": 100,
            "status": "STRONG"
        },

        "ETHUSDT": {
            "score": 0,
            "status": "WEAK"
        },

        "SOLUSDT": {
            "score": 100,
            "status": "STRONG"
        }
    }


    rebalance = PortfolioRebalancer()


    result = rebalance.rebalance(
        1000,
        report
    )


    print("\nREBALANCE:")
    print(result)


    assert len(result) == 3

    print(
        "\nPORTFOLIO REBALANCE V7.4 PASSED ✅"
    )


if __name__ == "__main__":
    run_test()
