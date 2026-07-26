from models.symbol_state import SymbolState
from brain.autonomous_execution_market_context import (
    AutonomousExecutionMarketContextV10_55
)

print(
    "========== DYNAMIC POSITION EXECUTION TEST V10.55 =========="
)

# 1. የቢናንስ እውነተኛ የገበያ ሁኔታ ማስመስያ ስቴት
state = SymbolState(
    symbol="BTCUSDT",
    exchange="BINANCE",
    last_price=50000
)

# 2. ኢንጂኑን ያለ ምንም የውጭ ጥገኝነት ማስነሳት
context_engine = AutonomousExecutionMarketContextV10_55()

# 3. ካፒታሉን በ build() ሜቶድ በኩል በግልጽ ማሳለፍ
context = context_engine.build(
    symbol_state=state,
    signal="BUY",
    capital=10000
)

print("EXECUTION CONTEXT:")
print(context)

# 4. የኢንቴግሬሽን ማረጋገጫዎች (Assertions)
assert context["symbol"] == "BTCUSDT"
assert context["side"] == "LONG"
assert context["execution_ready"] is True
assert context["size"] > 0
assert context["risk_amount"] > 0

print()
print(
    "✅ DYNAMIC POSITION EXECUTION TEST PASSED"
)
