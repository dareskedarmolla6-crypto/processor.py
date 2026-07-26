class AlphaUniverse:
    """
    AUTO MARKET INTELLIGENCE ENGINE

    - NO manual coin input
    - filters sideways noise
    - selects alpha + tradefi coins
    """

    def __init__(self):
        self.market_snapshot = {}

    # called by feed (later real API)
    def ingest(self, market_data):
        self.market_snapshot = market_data

    def score(self, symbol, data):

        volatility = data.get("volatility", 0)
        volume = data.get("volume", 0)
        trend = data.get("trend", 0)

        # ignore zero or negative movement coins (filters out completely stagnant assets)
        if volatility <= 0:
            return 0

        alpha_score = volatility * volume
        tradefi_score = trend * volume

        return alpha_score + tradefi_score

    def get_top_market(self, top_n=5):

        ranked = []

        for symbol, data in self.market_snapshot.items():
            score = self.score(symbol, data)
            if score > 0:
                ranked.append((symbol, score))

        ranked.sort(key=lambda x: x[1], reverse=True)

        return [s[0] for s in ranked[:top_n]]
