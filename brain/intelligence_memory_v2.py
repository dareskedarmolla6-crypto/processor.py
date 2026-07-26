"""
FSE Intelligence Memory V2

Production memory foundation for autonomous decision systems.

Responsibilities:
- Store decision experiences
- Replay historical knowledge
- Analyze performance
- Provide structured memory state
"""

# ማሻሻያ፡ timezone እዚህ ጋር ተጨምሯል
from datetime import datetime, timezone
from copy import deepcopy


class IntelligenceMemoryV2:
    """
    Persistent-ready intelligence memory layer.

    This layer keeps historical experiences in a
    structured format and provides controlled access.
    """

    def __init__(self):
        self.records = []
        self.sequence = 0

    def remember(
        self,
        decision,
        result
    ):
        """
        Store a completed decision experience.
        """
        self.sequence += 1

        # ማሻሻያ፡ ወደፊት የማይሰበር የUTC ጊዜ አወሳሰድ ተተክቷል
        record = {
            "id": self.sequence,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "symbol": decision.get("symbol"),
            "decision": decision.get("decision"),
            "confidence": decision.get("confidence", 0),
            "result": result
        }

        self.records.append(record)

        return {
            "status": "STORED",
            "id": self.sequence
        }

    def replay(
        self,
        symbol=None
    ):
        """
        Return historical records safely.
        """
        if symbol is None:
            return deepcopy(self.records)

        return deepcopy(
            [
                item
                for item in self.records
                if item["symbol"] == symbol
            ]
        )

    def analyze(self):
        """
        Calculate memory performance statistics.
        """
        total = len(self.records)

        wins = sum(
            1
            for item in self.records
            if item["result"] == "WIN"
        )

        losses = sum(
            1
            for item in self.records
            if item["result"] == "LOSS"
        )

        score = 0

        if total:
            score = round(
                (wins / total) * 100,
                2
            )

        return {
            "total_records": total,
            "wins": wins,
            "losses": losses,
            "performance_score": score
        }

    def state(self):
        return {
            "memory_size": len(self.records),
            "sequence": self.sequence
        }
