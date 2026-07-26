from risk.risk_manager import RiskGovernor


class MockStore:
    def __init__(self):
        self.data = {
            "system_status": "RUN"
        }

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)


def run_risk_governor_test():

    print("========== RISK GOVERNOR TEST ==========")

    # =========================
    # SETUP
    # =========================
    store = MockStore()
    governor = RiskGovernor(store)


    # =========================
    # TEST 1: NORMAL STATE
    # =========================
    result = governor.approve_trade()

    print("\nNORMAL:")
    print(result)

    assert result[0] is True


    # =========================
    # TEST 2: LOSS TRACKING
    # =========================
    print("\nLOSS TRACKING:")

    for i in range(5):
        governor.update(-10)
        print(
            f"Loss {i+1}:",
            governor.state
        )


    # =========================
    # TEST 3: SAFE MODE
    # =========================
    result = governor.approve_trade()

    print("\nAFTER LOSSES:")
    print(result)

    assert result[0] is False


    # =========================
    # TEST 4: EMERGENCY STOP
    # =========================
    store.set(
        "system_status",
        "EMERGENCY"
    )

    result = governor.approve_trade()

    print("\nEMERGENCY:")
    print(result)

    assert result[0] is False


    print("\nRISK GOVERNOR TEST PASSED ✅")


if __name__ == "__main__":
    run_risk_governor_test()
