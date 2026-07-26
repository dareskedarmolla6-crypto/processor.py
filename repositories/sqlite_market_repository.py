import sqlite3
from datetime import datetime

from models.symbol_state import SymbolState
from repositories.market_repository import MarketRepository


class SQLiteMarketRepository(MarketRepository):
    """
    SQLite persistence implementation.

    Responsibilities:
        - Persist validated SymbolState
        - Retrieve stored market state
        - Check symbol existence

    Does NOT contain:
        - Exchange communication
        - Market data generation
        - Trading logic
        - Strategy logic
    """

    def __init__(
        self,
        database_path: str = "market_state.db"
    ):
        self.database_path = database_path
        self._initialize()


    def _initialize(self):
        with sqlite3.connect(self.database_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS market_states (
                    symbol TEXT PRIMARY KEY,
                    exchange TEXT NOT NULL,
                    last_price REAL,
                    bid_price REAL,
                    ask_price REAL,
                    volume REAL,
                    timestamp TEXT NOT NULL,
                    market_status TEXT NOT NULL
                )
                """
            )


    def save(
        self,
        state: SymbolState
    ) -> None:

        with sqlite3.connect(self.database_path) as conn:

            conn.execute(
                """
                INSERT OR REPLACE INTO market_states
                (
                    symbol,
                    exchange,
                    last_price,
                    bid_price,
                    ask_price,
                    volume,
                    timestamp,
                    market_status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    state.symbol,
                    state.exchange,
                    state.last_price,
                    state.bid_price,
                    state.ask_price,
                    state.volume,
                    state.timestamp.isoformat(),
                    state.market_status,
                )
            )


    def get(
        self,
        symbol: str
    ):

        with sqlite3.connect(self.database_path) as conn:

            row = conn.execute(
                """
                SELECT
                    symbol,
                    exchange,
                    last_price,
                    bid_price,
                    ask_price,
                    volume,
                    timestamp,
                    market_status
                FROM market_states
                WHERE symbol = ?
                """,
                (symbol,)
            ).fetchone()

        if row is None:
            return None

        return SymbolState(
            symbol=row[0],
            exchange=row[1],
            last_price=row[2],
            bid_price=row[3],
            ask_price=row[4],
            volume=row[5],
            timestamp=datetime.fromisoformat(row[6]),
            market_status=row[7],
        )


    def exists(
        self,
        symbol: str
    ) -> bool:

        with sqlite3.connect(self.database_path) as conn:

            row = conn.execute(
                """
                SELECT 1
                FROM market_states
                WHERE symbol = ?
                """,
                (symbol,)
            ).fetchone()

        return row is not None
