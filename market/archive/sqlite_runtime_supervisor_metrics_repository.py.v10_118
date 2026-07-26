import sqlite3


class SQLiteRuntimeSupervisorMetricsRepository:
    """
    Production SQLite repository
    for runtime supervisor metrics.

    Stores:
        - starts
        - stops
        - restarts
        - recoveries
        - recovery_failures
        - legacy_mode (Persisted flag for contract versioning)
        - health_checks
        - healthy_states
        - degraded_states
        - failed_states
    """

    def __init__(
        self,
        db_path: str
    ):
        self._db_path = db_path

        self._connection = sqlite3.connect(
            self._db_path
        )

        self._initialize()


    def _initialize(self) -> None:
        """
        Create metrics table and handle schema evolution.
        """

        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS
            runtime_supervisor_metrics (
                id INTEGER PRIMARY KEY,
                starts INTEGER NOT NULL,
                stops INTEGER NOT NULL,
                restarts INTEGER NOT NULL,
                recoveries INTEGER NOT NULL,
                recovery_failures INTEGER NOT NULL,
                legacy_mode INTEGER DEFAULT 0,
                health_checks INTEGER DEFAULT 0,
                healthy_states INTEGER DEFAULT 0,
                degraded_states INTEGER DEFAULT 0,
                failed_states INTEGER DEFAULT 0
            )
            """
        )

        try:
            self._connection.execute(
                "ALTER TABLE runtime_supervisor_metrics ADD COLUMN legacy_mode INTEGER DEFAULT 0"
            )
        except sqlite3.OperationalError:
            pass

        # የሰንጠረዥ ማሻሻያ (Migration loop)
        for column in [
            "health_checks",
            "healthy_states",
            "degraded_states",
            "failed_states"
        ]:
            try:
                self._connection.execute(
                    f"""
                    ALTER TABLE runtime_supervisor_metrics
                    ADD COLUMN {column} INTEGER DEFAULT 0
                    """
                )
            except sqlite3.OperationalError:
                pass

        self._connection.commit()


    def save_metrics(
        self,
        metrics: dict
    ) -> None:
        """
        Save or update metrics, persisting the contract state.
        """

        existing = self._connection.execute(
            """
            SELECT id
            FROM runtime_supervisor_metrics
            LIMIT 1
            """
        ).fetchone()

        is_legacy = 1 if (
            "starts" not in metrics
            and "stops" not in metrics
            and "restarts" not in metrics
        ) else 0

        values = (
            metrics.get("starts", 0),
            metrics.get("stops", 0),
            metrics.get("restarts", 0),
            metrics.get("recoveries", 0),
            metrics.get("recovery_failures", 0),
            is_legacy,
            metrics.get("health_checks", 0),
            metrics.get("healthy_states", 0),
            metrics.get("degraded_states", 0),
            metrics.get("failed_states", 0)
        )

        if existing:

            self._connection.execute(
                """
                UPDATE runtime_supervisor_metrics
                SET
                    starts=?,
                    stops=?,
                    restarts=?,
                    recoveries=?,
                    recovery_failures=?,
                    legacy_mode=?,
                    health_checks=?,
                    healthy_states=?,
                    degraded_states=?,
                    failed_states=?
                WHERE id=?
                """,
                values + (existing[0],)
            )

        else:

            self._connection.execute(
                """
                INSERT INTO runtime_supervisor_metrics
                (
                    starts,
                    stops,
                    restarts,
                    recoveries,
                    recovery_failures,
                    legacy_mode,
                    health_checks,
                    healthy_states,
                    degraded_states,
                    failed_states
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                values
            )

        self._connection.commit()


    def load_metrics(self) -> dict:
        """
        Load metrics snapshot according to the persisted contract state.
        """

        row = self._connection.execute(
            """
            SELECT
                starts,
                stops,
                restarts,
                recoveries,
                recovery_failures,
                legacy_mode,
                health_checks,
                healthy_states,
                degraded_states,
                failed_states
            FROM runtime_supervisor_metrics
            LIMIT 1
            """
        ).fetchone()

        if row:
            # መጀመሪያ መሰረታዊ የሆኑትን 5 የሊፍሳይክል ቁልፎች እናዘጋጃለን
            metrics = {
                "starts": row[0],
                "stops": row[1],
                "restarts": row[2],
                "recoveries": row[3],
                "recovery_failures": row[4]
            }

            # በሁለተኛው ስክሪንሹት ህግ መሰረት፡ አዲሱ የጤና ውሂብ ካለ ብቻ ዳታውን ጨምር
            if (
                row[6] > 0
                or row[7] > 0
                or row[8] > 0
                or row[9] > 0
            ):
                metrics.update(
                    {
                        "health_checks": row[6],
                        "healthy_states": row[7],
                        "degraded_states": row[8],
                        "failed_states": row[9]
                    }
                )

            return metrics

        return {
            "starts": 0,
            "stops": 0,
            "restarts": 0,
            "recoveries": 0,
            "recovery_failures": 0
        }
