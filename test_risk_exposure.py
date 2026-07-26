from brain.risk_engine import RiskEngine

def run_risk_exposure_test():
    print("========== RISK EXPOSURE TEST (V2) ==========")

    # RiskEngine ን በተገቢው parameter አዋቅር
    risk = RiskEngine(max_risk_per_trade=0.03)
    balance = 1000

    # TEST 1: POSITION SIZE CALCULATION
    size = risk.calculate_position_size(
        balance=balance,
        entry_price=50,
        stop_loss_price=49
    )
    print(f"\nCalculated Size: {size}")
    assert size > 0

    # TEST 2: SAFE TRADE (Exposure Check)
    # ምንም ክፍት ፖዚሽን የለም፣ ስለዚህ መፈቀድ አለበት
    result = risk.check_trade(
        balance=balance,
        position_size=size,
        open_positions=[]
    )
    print(f"SAFE TRADE RESULT: {result}")
    assert result == "APPROVED"

    # TEST 3: HIGH EXPOSURE CHECK
    # 600 ሲሆን ከ 50% (500) በላይ ስለሆነ መታገድ አለበት
    large_position = 600
    result = risk.check_trade(
        balance=balance,
        position_size=large_position,
        open_positions=[]
    )
    print(f"HIGH EXPOSURE RESULT: {result}")
    assert result == "BLOCKED"

    print("\nRISK EXPOSURE TEST PASSED ✅")

if __name__ == "__main__":
    run_risk_exposure_test()
