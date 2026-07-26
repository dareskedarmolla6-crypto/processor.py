class PerformanceMemory:
    """
    FSE Performance Memory Engine V10.9
    Unified Learning Memory
    """

    def __init__(self):
        self.history = {}
        self.total_trades = 0
        self.wins = 0
        self.losses = 0


    def record(self, symbol, pnl):

        if symbol not in self.history:
            self.history[symbol] = {
                "trades": 0,
                "wins": 0,
                "losses": 0,
                "pnl": 0
            }

        data = self.history[symbol]

        data["trades"] += 1
        data["pnl"] += pnl

        self.total_trades += 1

        if pnl > 0:
            data["wins"] += 1
            self.wins += 1
        else:
            data["losses"] += 1
            self.losses += 1


    def record_result(
        self,
        symbol,
        win,
        pnl
    ):
        """
        Controller V10.9 learning callback
        """

        if win:
            pnl = abs(pnl) if pnl != 0 else 1
        else:
            pnl = -abs(pnl) if pnl != 0 else -1

        self.record(
            symbol,
            pnl
        )

        return {
            "status": "LEARNED"
        }


    def score(self, symbol):

        if symbol not in self.history:
            return 0

        data = self.history[symbol]

        if data["trades"] == 0:
            return 0

        return round(
            (data["wins"] / data["trades"]) * 100,
            2
        )


    def adjust_confidence(
        self,
        symbol,
        confidence
    ):

        score = self.score(symbol)

        if score >= 80:
            confidence += 0.10

        elif score < 40:
            confidence -= 0.10

        return max(
            0,
            min(
                round(confidence,2),
                1
            )
        )


    def get(self):

        return {
            "history": self.history,
            "total_trades": self.total_trades,
            "wins": self.wins,
            "losses": self.losses
        }
