import sqlite3

from .runtime_event_repository import RuntimeEventRepository


class SQLiteRuntimeEventRepository(
    RuntimeEventRepository
):
    """
    SQLite implementation for runtime event persistence.

    Responsibilities:
        - Persist runtime lifecycle events
        - Restore event history

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
        Create event storage table.
        """

        with sqlite3.connect(
            self._db_path
        ) as conn:

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS runtime_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            conn.commit()


    def save_event(
        self,
        event: str
    ) -> None:
        """
        Persist runtime event.
        """

        with sqlite3.connect(
            self._db_path
        ) as conn:

            conn.execute(
                """
                INSERT INTO runtime_events(event)
                VALUES(?)
                """,
                (event,)
            )

            conn.commit()


    def load_events(
        self
    ) -> list:
        """
        Restore runtime event history.
        """

        with sqlite3.connect(
            self._db_path
        ) as conn:

            cursor = conn.execute(
                """
                SELECT event
                FROM runtime_events
                ORDER BY id ASC
                """
            )

            return [
                row[0]
                for row in cursor.fetchall()
            ]
