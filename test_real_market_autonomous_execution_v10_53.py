from clients.binance_client import BinanceClient
from clients.binance_market_data_client import BinanceMarketDataClient

from market.real_market_feed_adapter import RealMarketFeedAdapter

from brain.autonomous_execution_market_context import (
    AutonomousExecutionMarketContextV10_52
)

from brain.execution_engine import ExecutionEngine
from brain.execution_persistence import ExecutionPersistence


print(
    "========== REAL MARKET AUTONOMOUS EXECUTION V10.53 =========="
)


# --------------------------------------------------
# REAL MARKET DATA
# --------------------------------------------------

client = BinanceClient()

market_client = BinanceMarketDataClient(
    client
)


feed = RealMarketFeedAdapter(
    market_client,
    [
        "BTCUSDT"
    ]
)


snapshot = feed.fetch()


print(
    "MARKET SNAPSHOT:"
)

print(snapshot)


# --------------------------------------------------
# SYMBOL STATE FROM REAL FEED
# --------------------------------------------------

from models.symbol_state import SymbolState


item = snapshot[0]


state = SymbolState(
    symbol=item["symbol"],
    exchange=item["exchange"],
    last_price=item["price"]
)



# --------------------------------------------------
# EXECUTION CONTEXT
# --------------------------------------------------

context_builder = AutonomousExecutionMarketContextV10_52()


context = context_builder.build(
    state,
    "BUY",
    size=1.0
)


print(
    "EXECUTION CONTEXT:"
)

print(context)



assert context["side"] == "LONG"
assert context["execution_ready"] is True



# --------------------------------------------------
# EXECUTION ENGINE
# --------------------------------------------------

persistence = ExecutionPersistence()


engine = ExecutionEngine(
    persistence=persistence
)


position = engine.open(
    context["symbol"],
    context["side"],
    context["size"],
    context["price"]
)


print(
    "POSITION:"
)

print(position)



assert position["status"] == "OPEN"
assert position["symbol"] == "BTCUSDT"



print(
    "\n✅ REAL MARKET AUTONOMOUS EXECUTION TEST PASSED"
)
