import sqlite3

from .runtime_metrics_repository import (
    RuntimeMetricsRepository
)


class SQLiteRuntimeMetricsRepository(
    RuntimeMetricsRepository
):
    """
    SQLite implementation for runtime metrics persistence.

    Responsibilities:
        - Persist runtime metrics
        - Restore runtime metrics

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
        Create metrics storage.
        """

        with sqlite3.connect(
            self._db_path
        ) as conn:

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS
                runtime_metrics (
                    id INTEGER PRIMARY KEY,
                    successful_cycles INTEGER NOT NULL,
                    failed_cycles INTEGER NOT NULL
                )
                """
            )

            conn.commit()


    def save_metrics(
        self,
        metrics: dict
    ) -> None:
        """
        Persist metrics snapshot.
        """

        with sqlite3.connect(
            self._db_path
        ) as conn:

            conn.execute(
                """
                DELETE FROM runtime_metrics
                """
            )

            conn.execute(
                """
                INSERT INTO runtime_metrics(
                    id,
                    successful_cycles,
                    failed_cycles
                )
                VALUES(1, ?, ?)
                """,
                (
                    metrics.get(
                        "successful_cycles",
                        0
                    ),
                    metrics.get(
                        "failed_cycles",
                        0
                    )
                )
            )

            conn.commit()


    def load_metrics(
        self
    ) -> dict:
        """
        Restore metrics snapshot.
        """

        with sqlite3.connect(
            self._db_path
        ) as conn:

            cursor = conn.execute(
                """
                SELECT
                    successful_cycles,
                    failed_cycles
                FROM runtime_metrics
                WHERE id = 1
                """
            )

            row = cursor.fetchone()

            if not row:
                return {}

            return {
                "successful_cycles": row[0],
                "failed_cycles": row[1]
            }
