from brain.market_regime import MarketRegime


def run_test():

    print("========== MARKET REGIME V9.0 ==========")

    analyzer = MarketRegime()

    # -------------------------
    # TRENDING
    # -------------------------
    trending = analyzer.analyze({
        "trend": 0.9,
        "volatility": 0.2
    })

    print("\nTRENDING:")
    print(trending)

    assert trending["regime"] == "TRENDING"
    assert trending["risk_multiplier"] == 1.2

    # -------------------------
    # VOLATILE
    # -------------------------
    volatile = analyzer.analyze({
        "trend": 0.3,
        "volatility": 0.9
    })

    print("\nVOLATILE:")
    print(volatile)

    assert volatile["regime"] == "VOLATILE"
    assert volatile["risk_multiplier"] == 0.7

    # -------------------------
    # RANGING
    # -------------------------
    ranging = analyzer.analyze({
        "trend": 0.4,
        "volatility": 0.4
    })

    print("\nRANGING:")
    print(ranging)

    assert ranging["regime"] == "RANGING"
    assert ranging["risk_multiplier"] == 1.0

    print("\nMARKET REGIME V9.0 PASSED ✅")


if __name__ == "__main__":
    run_test()
