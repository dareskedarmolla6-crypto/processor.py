from brain.position_sizing_engine import PositionSizingEngine


print(
    "========== POSITION SIZING TEST V10.54 =========="
)


engine = PositionSizingEngine(
    max_risk_percent=0.02
)


result = engine.calculate(
    capital=10000,
    price=50000
)


print(result)


assert result["capital"] == 10000
assert result["risk_percent"] == 0.02
assert result["risk_amount"] == 200
assert result["size"] == 0.004


print(
    "\n✅ POSITION SIZING TEST PASSED"
)
