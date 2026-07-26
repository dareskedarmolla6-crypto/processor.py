class MarketRegime:
    """
    FSE Market Regime Analyzer V9.1

    Supports:
    - Manual regime selection
    - Automatic market analysis
    """

    def __init__(self):

        self.current = {
            "regime": "RANGING",
            "risk_multiplier": 1.0,
            "confidence_bonus": 0.0
        }

    # ---------------------------------
    # Automatic Analysis
    # ---------------------------------

    def analyze(self, market):

        trend = market.get("trend", 0)
        volatility = market.get("volatility", 0)

        if trend >= 0.7 and volatility <= 0.5:

            self.current = {
                "regime": "TRENDING",
                "risk_multiplier": 1.2,
                "confidence_bonus": 0.05
            }

        elif volatility >= 0.7:

            self.current = {
                "regime": "VOLATILE",
                "risk_multiplier": 0.7,
                "confidence_bonus": -0.05
            }

        else:

            self.current = {
                "regime": "RANGING",
                "risk_multiplier": 1.0,
                "confidence_bonus": 0.0
            }

        return self.current

    # ---------------------------------
    # Manual Override
    # ---------------------------------

    def set_regime(self, regime):

        table = {

            "TRENDING": {
                "regime": "TRENDING",
                "risk_multiplier": 1.2,
                "confidence_bonus": 0.05
            },

            "VOLATILE": {
                "regime": "VOLATILE",
                "risk_multiplier": 0.7,
                "confidence_bonus": -0.05
            },

            "RANGING": {
                "regime": "RANGING",
                "risk_multiplier": 1.0,
                "confidence_bonus": 0.0
            }

        }

        self.current = table.get(
            regime,
            table["RANGING"]
        )

    # ---------------------------------
    # Current State
    # ---------------------------------

    def get_current(self):

        return self.current
