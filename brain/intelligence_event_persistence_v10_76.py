import json
import sqlite3
from datetime import datetime, UTC


class IntelligenceEventPersistenceV10_76:
    """
    FSE Intelligence Event Persistence V10.76

    Responsibilities
    ----------------
    - Persist intelligence events in a SQLite database
    - Retrieve event history reliably

    Does NOT contain
    ----------------
    - Learning logic
    - Decision logic
    - Execution logic
    """

    def __init__(
        self,
        database="fse_intelligence.db"
    ):
        self.database = database
        self._initialize()


    def _initialize(self):
        """
        Initializes the SQLite database and creates the table if it doesn't exist.
        """
        conn = sqlite3.connect(self.database)
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS intelligence_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_data TEXT NOT NULL,
                    stored_at TEXT NOT NULL
                )
                """
            )
            conn.commit()
        finally:
            conn.close()


    def save(
        self,
        event
    ):
        """
        Saves an event by converting it to JSON and inserting it into SQLite.
        """
        now = datetime.now(UTC).isoformat()
        event_json = json.dumps(event)

        conn = sqlite3.connect(self.database)
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO intelligence_events (event_data, stored_at)
                VALUES (?, ?)
                """,
                (event_json, now)
            )
            conn.commit()
        finally:
            conn.close()

        return {
            "event": event,
            "stored_at": now
        }


    def load_all(self):
        """
        Retrieves all intelligence events from SQLite database.
        """
        conn = sqlite3.connect(self.database)
        events = []
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT event_data, stored_at 
                FROM intelligence_events 
                ORDER BY id ASC
                """
            )
            rows = cursor.fetchall()
            for row in rows:
                events.append({
                    "event": json.loads(row[0]),
                    "stored_at": row[1]
                })
        finally:
            conn.close()

        return events
