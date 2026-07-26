import sqlite3
import os


class PersistentMemory:
    """
    FSE Persistent Learning Memory

    Stores:
    - Trade history
    - Wins / Losses
    - PNL
    - Symbol performance

    RAM Memory
          ↓
    SQLite Storage
          ↓
    Reload Learning
    """


    def __init__(
        self,
        db_path="fse_memory.db"
    ):

        self.db_path = db_path

        self.conn = sqlite3.connect(
            self.db_path
        )

        self.create_table()



    # -------------------------
    # Create Database
    # -------------------------
    def create_table(self):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS performance
            (
                symbol TEXT PRIMARY KEY,
                trades INTEGER,
                wins INTEGER,
                losses INTEGER,
                pnl REAL
            )
            """
        )

        self.conn.commit()



    # -------------------------
    # Save Result
    # -------------------------
    def save_trade(
        self,
        symbol,
        pnl
    ):

        cursor = self.conn.cursor()


        row = cursor.execute(
            """
            SELECT *
            FROM performance
            WHERE symbol=?
            """,
            (symbol,)
        ).fetchone()



        if row:

            trades = row[1] + 1
            wins = row[2]
            losses = row[3]
            total_pnl = row[4] + pnl


            if pnl > 0:
                wins += 1
            else:
                losses += 1


            cursor.execute(
                """
                UPDATE performance

                SET trades=?,
                    wins=?,
                    losses=?,
                    pnl=?

                WHERE symbol=?
                """,
                (
                    trades,
                    wins,
                    losses,
                    total_pnl,
                    symbol
                )
            )


        else:

            cursor.execute(
                """
                INSERT INTO performance
                VALUES(?,?,?,?,?)
                """,
                (
                    symbol,
                    1,
                    1 if pnl > 0 else 0,
                    0 if pnl > 0 else 1,
                    pnl
                )
            )


        self.conn.commit()



    # -------------------------
    # Load History
    # -------------------------
    def load_history(self):

        cursor = self.conn.cursor()

        rows = cursor.execute(
            """
            SELECT *
            FROM performance
            """
        ).fetchall()


        history = {}


        for row in rows:

            history[row[0]] = {

                "trades": row[1],
                "wins": row[2],
                "losses": row[3],
                "pnl": row[4]

            }


        return history



    # -------------------------
    # Close DB
    # -------------------------
    def close(self):

        self.conn.close()
