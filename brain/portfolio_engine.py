class PortfolioEngine:
    """
    PORTFOLIO MANAGEMENT ENGINE
    controls capital allocation and position sizing
    """

    def __init__(self):
        self.risk_ratio = 0.1


    def get_state(self, balance):
        return {
            "balance": balance,
            "risk_ratio": self.risk_ratio
        }


    def calculate_size(self, balance, state):
        return balance * self.risk_ratio
