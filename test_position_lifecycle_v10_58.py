from brain.execution_engine import ExecutionEngine
from brain.position_manager import PositionManager
from brain.price_monitor import PriceMonitor


print(
    "========== POSITION LIFECYCLE TEST V10.58 =========="
)


execution = ExecutionEngine()

manager = PositionManager(
    execution
)

monitor = PriceMonitor(
    manager
)


# Open position
position = execution.open(
    symbol="BTCUSDT",
    side="LONG",
    size=1.0,
    price=50000
)


assert position["status"] == "OPEN"


# Price update with profit
result = monitor.update(
    "BTCUSDT",
    55000
)


print("MONITOR RESULT:")
print(result)


assert len(result) == 1


# Check SmartExit response exists
assert "result" in result[0]


print()

print(
    "✅ POSITION LIFECYCLE TEST PASSED"
)
