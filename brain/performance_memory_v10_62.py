from datetime import datetime, UTC


class PerformanceMemoryV10_62:
    """
    FSE Production Performance Memory V10.62

    Responsibilities
    ----------------
    - Store completed trade feedback
    - Maintain execution history
    - Calculate performance statistics
    - Provide learning data

    Does NOT contain:
    - Strategy decisions
    - Market prediction
    - Fake data generation
    """


    def __init__(self):

        self.records = []


    def store(
        self,
        feedback: dict
    ):

        if not feedback:
            raise ValueError(
                "Feedback record required"
            )


        record = {
            **feedback,
            "stored_at": datetime.now(
                UTC
            ).isoformat()
        }


        self.records.append(
            record
        )


        return record



    def statistics(self):

        total = len(
            self.records
        )


        wins = sum(
            1
            for r in self.records
            if r["outcome"] == "WIN"
        )


        losses = sum(
            1
            for r in self.records
            if r["outcome"] == "LOSS"
        )


        pnl = sum(
            r["realized_pnl"]
            for r in self.records
        )


        win_rate = (
            wins / total
            if total > 0
            else 0.0
        )


        return {
            "total_trades": total,
            "wins": wins,
            "losses": losses,
            "win_rate": win_rate,
            "total_pnl": pnl
        }
