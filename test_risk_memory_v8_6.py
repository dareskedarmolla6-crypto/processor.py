from brain.risk_adapter import RiskAdapter
from brain.self_correction import SelfCorrection


def run_test():

    print("========== RISK MEMORY V8.6 ==========")


    correction = SelfCorrection()


    adapter = RiskAdapter()


    print("\nINITIAL RISK:")
    print(adapter.get_risk())


    result = correction.analyze(
        [
            {
                "symbol":"BTCUSDT",
                "pnl":100
            }
        ]
    )


    adapter.apply_correction(
        result
    )


    print("\nAFTER WIN:")
    print(adapter.get_risk())


    assert adapter.get_risk() == 0.04


    # simulate restart
    new_adapter = RiskAdapter()


    print("\nAFTER RESTART:")
    print(new_adapter.get_risk())


    assert new_adapter.get_risk() == 0.04


    print("\nRISK MEMORY V8.6 PASSED ✅")


if __name__ == "__main__":
    run_test()
