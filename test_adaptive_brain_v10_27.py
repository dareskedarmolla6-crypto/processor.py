from brain.adaptive_brain_v10_27 import AdaptiveBrainV10_27


def run_test():

    print(
        "========== ADAPTIVE BRAIN V10.27 =========="
    )


    brain = AdaptiveBrainV10_27()


    optimizer_state = {
        "confidence_threshold":0.85,
        "risk_level":0.04,
        "mode":"AGGRESSIVE"
    }


    updated = brain.update(
        optimizer_state
    )


    print("\nUPDATED:")
    print(updated)



    decision = brain.decide(
        {
            "symbol":"BTCUSDT",
            "signal":"BUY",
            "confidence":0.90
        }
    )


    print("\nDECISION:")
    print(decision)


    assert decision["decision"] == "TRADE"
    assert decision["mode"] == "AGGRESSIVE"


    print(
        "\nADAPTIVE BRAIN V10.27 PASSED ✅"
    )


if __name__ == "__main__":
    run_test()
