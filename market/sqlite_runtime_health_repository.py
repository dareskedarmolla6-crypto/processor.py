import sqlite3

from .runtime_health_repository import (
    RuntimeHealthRepository
)


class SQLiteRuntimeHealthRepository(
    RuntimeHealthRepository
):
    """
    SQLite implementation for runtime health persistence.

    Responsibilities:
        - Persist runtime health snapshot
        - Restore runtime health snapshot

    Does NOT contain:
        - Runtime control logic
        - Scheduler logic
        - Market data logic
        - Trading decisions
    """

    def __init__(
        self,
        db_path: str
    ):
        self._db_path = db_path

        self._initialize()


    def _initialize(
        self
    ) -> None:
        """
        Create health storage table.
        """

        with sqlite3.connect(
            self._db_path
        ) as conn:

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS runtime_health (
                    id INTEGER PRIMARY KEY,
                    status TEXT NOT NULL,
                    healthy INTEGER NOT NULL,
                    cycles INTEGER NOT NULL,
                    last_error TEXT
                )
                """
            )

            conn.commit()


    def save_health(
        self,
        health: dict
    ) -> None:
        """
        Persist health snapshot.
        """

        with sqlite3.connect(
            self._db_path
        ) as conn:

            conn.execute(
                """
                INSERT OR REPLACE INTO runtime_health
                (
                    id,
                    status,
                    healthy,
                    cycles,
                    last_error
                )
                VALUES
                (
                    1,
                    ?,
                    ?,
                    ?,
                    ?
                )
                """,
                (
                    health["status"],
                    int(health["healthy"]),
                    health["cycles"],
                    health["last_error"]
                )
            )

            conn.commit()


    def load_health(
        self
    ) -> dict:
        """
        Restore health snapshot.
        """

        with sqlite3.connect(
            self._db_path
        ) as conn:

            cursor = conn.execute(
                """
                SELECT
                    status,
                    healthy,
                    cycles,
                    last_error
                FROM runtime_health
                WHERE id = 1
                """
            )

            row = cursor.fetchone()

            if not row:
                return {}

            return {
                "status": row[0],
                "healthy": bool(row[1]),
                "cycles": row[2],
                "last_error": row[3]
            }
