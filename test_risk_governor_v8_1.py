from brain.risk_governor import RiskGovernor
from brain.risk_adapter import RiskAdapter


def run_test():

    print("========== RISK GOVERNOR V8.1 ==========")


    adapter = RiskAdapter()

    adapter.apply_correction(
        {
            "risk_adjustment": 0.02,
            "action": "IMPROVE"
        }
    )


    governor = RiskGovernor(
        risk_adapter=adapter
    )


    result = governor.approve(
        "BTCUSDT",
        500,
        "NORMAL",
        1000,
        []
    )


    print("\nAPPROVAL:")
    print(result)


    assert result["decision"] == "APPROVED"
    assert result["risk"] == 0.05


    print("\nRISK GOVERNOR V8.1 PASSED ✅")


if __name__ == "__main__":
    run_test()
