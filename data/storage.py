# fse/data/storage_handler.py
import json
import time
import logging

logger = logging.getLogger(__name__)

class InMemoryStore:
    """
    የቦቱ ማህደረ ትውስታ (System State, Trades, Positions)።
    """

    def __init__(self):
        self.data = {
            "system_status": "RUNNING",
            "trades": [],
            "positions": [],
            "logs": []
        }

    # =========================
    # SYSTEM STATUS
    # =========================
    def set_status(self, status: str):
        self.data["system_status"] = status

    def get(self, key):
        return self.data.get(key)

    # =========================
    # TRADE STORAGE
    # =========================
    def save_trade(self, trade: dict):
        trade["ts"] = int(time.time())
        self.data["trades"].append(trade)

    def get_trades(self):
        return self.data["trades"]

    # =========================
    # POSITION STORAGE
    # =========================
    def save_position(self, position: dict):
        position["ts"] = int(time.time())
        self.data["positions"].append(position)

    def get_positions(self):
        return self.data["positions"]

    # =========================
    # LOGS
    # =========================
    def log(self, message: str):
        self.data["logs"].append({
            "message": message,
            "ts": int(time.time())
        })

    def get_logs(self):
        return self.data["logs"]

    # =========================
    # RELIABILITY ENGINE
    # =========================
    def get_active_trades(self):
        return [
            t for t in self.data["trades"]
            if t.get("status") != "CLOSED"
        ]

    def update_trade_status(self, trade_id: str, status: str):
        """
        Update trade status safely.
        """
        for trade in self.data["trades"]:
            if trade.get("trade_id") == trade_id:
                trade["status"] = status
                trade["updated_ts"] = int(time.time())
                logger.info(
                    f"Trade {trade_id} updated to {status}"
                )
                return True

        logger.warning(
            f"Trade {trade_id} not found."
        )
        return False

    # =========================
    # FILE I/O WITH SAFETY GUARDS
    # =========================
    def save_to_file(self, path="fse_storage.json"):
        """ውሂብን በደህና ወደ ፋይል መጻፍ።"""
        try:
            with open(path, "w") as f:
                json.dump(self.data, f, indent=4)
            logger.info(f"✅ Data saved to {path}")
        except Exception as e:
            logger.error(f"❌ Failed to save data: {e}")
            raise

    def safe_save_to_file(self, path="fse_storage.json"):
        """የተበላሸ ፋይል እንዳይፈጠር Backup መስሪያ።"""
        backup_path = path + ".backup"
        try:
            self.save_to_file(path)
        except Exception:
            logger.warning(
                "⚠️ Primary save failed. Saving to backup..."
            )
            self.save_to_file(backup_path)

    def load_from_file(self, path="fse_storage.json"):
        """ከፋይል ውሂብን መጫን።"""
        try:
            with open(path, "r") as f:
                self.data = json.load(f)
            logger.info("✅ Data loaded successfully.")
        except FileNotFoundError:
            logger.info("No existing storage file found. Starting with empty storage.")
        except json.JSONDecodeError as e:
            logger.error(f"Storage file is corrupted: {e}")
import json
