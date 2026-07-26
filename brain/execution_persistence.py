import sqlite3


class ExecutionPersistence:
    """
    Production execution persistence layer.

    Responsibilities:
    - Save opened positions
    - Update closed positions
    - Restore positions after restart

    No fake data.
    No simulation logic.
    Real persistence only.
    """

    def __init__(self, db_path="fse_data.db"):

        self.db_path = db_path

        self._init_table()


    def _connect(self):

        return sqlite3.connect(
            self.db_path
        )


    def _init_table(self):

        with self._connect() as conn:

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS execution_positions (

                    id INTEGER PRIMARY KEY,

                    symbol TEXT NOT NULL,

                    side TEXT NOT NULL,

                    size REAL NOT NULL,

                    entry REAL NOT NULL,

                    status TEXT NOT NULL,

                    realized_pnl REAL DEFAULT 0,

                    entry_time TEXT,

                    exit_price REAL,

                    exit_time TEXT,

                    close_reason TEXT
                )
                """
            )


    def save_position(self, position):

        with self._connect() as conn:

            conn.execute(
                """
                INSERT OR REPLACE INTO execution_positions
                (
                    id,
                    symbol,
                    side,
                    size,
                    entry,
                    status,
                    realized_pnl,
                    entry_time
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,

                (
                    position["id"],
                    position["symbol"],
                    position["side"],
                    position["size"],
                    position["entry"],
                    position["status"],
                    position["realized_pnl"],
                    position["entry_time"]
                )
            )


    def close_position(
        self,
        position
    ):

        with self._connect() as conn:

            conn.execute(
                """
                UPDATE execution_positions

                SET
                    status=?,
                    realized_pnl=?,
                    exit_price=?,
                    exit_time=?,
                    close_reason=?

                WHERE id=?
                """,

                (
                    position["status"],
                    position["realized_pnl"],
                    position["exit"],
                    position["exit_time"],
                    position["close_reason"],
                    position["id"]
                )
            )


    # --------------------------------------------------
    # UPDATE POSITION
    # --------------------------------------------------
    def update_position(
        self,
        position
    ):

        with self._connect() as conn:

            conn.execute(
                """
                UPDATE execution_positions
                SET
                    size=?,
                    status=?,
                    realized_pnl=?
                WHERE id=?
                """,
                (
                    position["size"],
                    position["status"],
                    position["realized_pnl"],
                    position["id"]
                )
            )


    # --------------------------------------------------
    # RESTORE POSITIONS (UPDATED WITH OPEN FILTER) ✅
    # --------------------------------------------------
    def restore_positions(self):

        with self._connect() as conn:

            rows = conn.execute(
                """
                SELECT
                    id,
                    symbol,
                    side,
                    size,
                    entry,
                    status,
                    realized_pnl,
                    entry_time,
                    exit_price,
                    exit_time,
                    close_reason
                FROM execution_positions
                WHERE status='OPEN'
                """
            )

            positions = []

            for row in rows.fetchall():

                positions.append({
                    "id": row[0],
                    "symbol": row[1],
                    "side": row[2],
                    "size": row[3],
                    "entry": row[4],
                    "status": row[5],
                    "realized_pnl": row[6],
                    "entry_time": row[7],
                    "last_update": row[7],
                    "highest_price": row[4],
                    "lowest_price": row[4],
                    "locked_profit": 0.0,
                    "trailing_price": None,
                    "stop_loss": None,
                    "exit": row[8],
                    "exit_time": row[9],
                    "close_reason": row[10]
                })

            return positions
