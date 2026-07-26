class MarketScanner:
    """
    FSE Market Scanner

    - Scan market symbols
    - Filter opportunities
    - Generate BUY / SELL signals
    """

    def __init__(self, min_confidence=0.70):
        self.min_confidence = min_confidence

    def scan(self, market_data):

        opportunities = []

        for item in market_data:

            symbol = item["symbol"]
            price = item["price"]
            confidence = item["confidence"]
            signal = item["signal"]

            if confidence >= self.min_confidence:
                opportunities.append({
                    "symbol": symbol,
                    "price": price,
                    "signal": signal,
                    "confidence": confidence
                })

        return opportunities
