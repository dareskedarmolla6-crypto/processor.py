from brain.portfolio_rebalancer_v9_6 import PortfolioRebalancerV9_6


def run_test():

    print("========== PORTFOLIO REBALANCER V9.6 ==========")


    rebalancer = PortfolioRebalancerV9_6()


    allocations = [

        {
            "symbol": "BTCUSDT",
            "allocation": 600
        },

        {
            "symbol": "ETHUSDT",
            "allocation": 400
        }

    ]


    result = rebalancer.rebalance(
        allocations,
        "TRENDING",
        0.05
    )


    print("\nTRENDING:")
    print(result)


    assert result[0]["rebalance"] == 576.0
    assert result[1]["rebalance"] == 384.0



    volatile = rebalancer.rebalance(
        allocations,
        "VOLATILE",
        0.03
    )


    print("\nVOLATILE:")
    print(volatile)


    assert volatile[0]["rebalance"] == 336.0


    print(
        "\nPORTFOLIO REBALANCER V9.6 PASSED ✅"
    )


if __name__ == "__main__":
    run_test()
