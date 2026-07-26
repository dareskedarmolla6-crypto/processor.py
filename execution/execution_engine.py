import time
import uuid
import hashlib
import logging
from execution.connection_tester import test_api_connection

logger = logging.getLogger(__name__)


# ==========================================================
# IDEMPOTENCY KEY
# ==========================================================
def generate_idempotency_key(symbol, side, qty, strategy_id, bucket):
    raw = f"{symbol}:{side}:{qty}:{strategy_id}:{bucket}"
    return hashlib.sha256(raw.encode()).hexdigest()


# ==========================================================
# BINANCE GATEWAY
# ==========================================================
class BinanceGateway:

    MAX_LEVERAGE = 70

    def __init__(self, client):
        self.client = client

    def place_order(
        self,
        symbol,
        side,
        qty,
        leverage=0,
        idempotency_key=None
    ):
        try:
            leverage = min(
                max(int(leverage), 0),
                self.MAX_LEVERAGE
            )

            if leverage > 0:
                self.client.futures_change_leverage(
                    symbol=symbol,
                    leverage=leverage
                )

            return self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=qty,
                newClientOrderId=idempotency_key
            )

        except Exception as e:
            logger.error(
                f"❌ Order placement failed: {e}"
            )
            return None

    def query_order(self, symbol, order_id):
        try:
            return self.client.futures_get_order(
                symbol=symbol,
                orderId=order_id
            )
        except Exception as e:
            logger.error(
                f"❌ Order query failed: {e}"
            )
            return None

    def close_position(self, symbol):
        try:
            pos = self.client.futures_position_information(
                symbol=symbol
            )

            if not pos:
                return None

            amount = float(
                pos[0]["positionAmt"]
            )

            if amount == 0:
                return None

            qty = abs(amount)

            side = (
                "SELL"
                if amount > 0
                else "BUY"
            )

            return self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=qty
            )

        except Exception as e:
            logger.error(
                f"❌ Close position failed: {e}"
            )
            return None


# ==========================================================
# EXECUTION COORDINATOR
# ==========================================================
class ExecutionCoordinator:

    def __init__(
        self,
        risk_engine,
        gateway,
        store
    ):
        self.risk = risk_engine
        self.gateway = gateway
        self.store = store

    def execute_signal(self, signal):
        if not test_api_connection():
            logger.critical(
                "🚨 CONNECTION LOST"
            )
            raise Exception(
                "SYSTEM HALTED - NO CONNECTION"
            )

        if self.store.get(
            "system_status"
        ) in ["STOP", "EMERGENCY"]:
            raise Exception(
                "SYSTEM HALTED - EMERGENCY STOP"
            )

        approved, reason = self.risk.validate_new_position(
            signal.get("side"),
            signal.get("balance", 0),
            signal.get("qty", 0),
            []
        )

        if not approved:
            logger.warning(
                f"⚠️ Signal rejected by Risk Engine: {reason}"
            )
            return None

        trade_id = (
            f"BOT_{uuid.uuid4().hex[:16]}"
        )

        key = generate_idempotency_key(
            signal["symbol"],
            signal["side"],
            signal["qty"],
            signal["strategy_id"],
            int(time.time() // 60)
        )

        response = self.gateway.place_order(
            signal["symbol"],
            signal.get(
                "exchange_side",
                signal["side"]
            ),
            signal["qty"],
            signal.get(
                "leverage",
                0
            ),
            key
        )

        if response:

            logger.info(
                f"BINANCE RESPONSE TYPE: {type(response)}"
            )

            logger.info(
                f"BINANCE RESPONSE: {response}"
            )

            if (
                isinstance(response, dict)
                and response.get("status", 200) != 200
                and "orderId" not in response
            ):
                logger.error(
                    f"❌ Binance rejected order: {response}"
                )
                return None

            order_id = response.get(
                "orderId"
            )

            if not order_id:
                logger.error(
                    "❌ Invalid Binance response"
                )
                return None

            self.store.save_trade({
                "trade_id": trade_id,
                "order_id": order_id,
                "symbol": signal["symbol"],
                "status": "OPEN",
                "ts": time.time()
            })

            return {
                "trade_id": trade_id,
                "order_id": order_id,
                "symbol": signal["symbol"],
                "status": "SUBMITTED"
            }

        return None


# ==========================================================
# LIVE SYNC ENGINE
# ==========================================================
class LiveSyncEngine:

    def __init__(
        self,
        gateway,
        store
    ):
        self.gateway = gateway
        self.store = store

    def sync(self):

        for trade in self.store.get_active_trades():
            order = self.gateway.query_order(
                trade["symbol"],
                trade["order_id"]
            )

            if order and order.get("status") == "FILLED":
                logger.info(
                    f"✅ Trade {trade['trade_id']} synced"
                )
