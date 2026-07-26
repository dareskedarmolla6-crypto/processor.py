import sqlite3
from market.runtime_state_repository import (
    RuntimeStateRepository
)


class SQLiteRuntimeStateRepository(
    RuntimeStateRepository
):
    """
    Production SQLite runtime state repository.

    Responsibilities:
        - Persist runtime state
        - Restore runtime state

    Does NOT contain:
        - Runtime control logic
        - Scheduler logic
        - Market data logic
    """

    def __init__(
        self,
        db_path
    ):

        self._connection = sqlite3.connect(
            db_path
        )

        self._create_table()


    def _create_table(
        self
    ):

        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS runtime_state (
                id INTEGER PRIMARY KEY,
                status TEXT NOT NULL,
                cycles INTEGER NOT NULL,
                last_error TEXT
            )
            """
        )

        self._connection.commit()


    def save_state(
        self,
        state: dict
    ) -> None:

        self._connection.execute(
            """
            DELETE FROM runtime_state
            """
        )

        self._connection.execute(
            """
            INSERT INTO runtime_state
            (
                id,
                status,
                cycles,
                last_error
            )
            VALUES
            (
                1,
                ?,
                ?,
                ?
            )
            """,
            (
                state["status"],
                state["cycles"],
                state["last_error"]
            )
        )

        self._connection.commit()


    def load_state(
        self
    ) -> dict:

        cursor = self._connection.execute(
            """
            SELECT
                status,
                cycles,
                last_error
            FROM runtime_state
            WHERE id = 1
            """
        )

        row = cursor.fetchone()

        if row is None:
            return {}

        return {
            "status": row[0],
            "cycles": row[1],
            "last_error": row[2]
        }
