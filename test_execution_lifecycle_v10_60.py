from brain.execution_engine import ExecutionEngine
from brain.position_manager import PositionManager
from brain.price_monitor import PriceMonitor


print(
    "========== EXECUTION LIFECYCLE TEST V10.60 =========="
)


execution = ExecutionEngine()


position = execution.open(
    "BTCUSDT",
    "LONG",
    0.2,
    50000
)


manager = PositionManager(
    execution
)


monitor = PriceMonitor(
    manager
)


result = monitor.update(
    "BTCUSDT",
    55000
)


print("MONITOR RESULT:")
print(result)


# ከእንግዲህ ትክክለኛውን ሁኔታ ለማረጋገጥ ከኢንጂኑ ስቴት ላይ ወቅታዊውን መረጃ እንወስዳለን
updated_position = execution.positions["BTCUSDT"][0]


assert updated_position["status"] == "OPEN"


assert (
    updated_position["highest_price"]
    == 55000
)


print()

print(
    "✅ EXECUTION LIFECYCLE TEST PASSED"
)
