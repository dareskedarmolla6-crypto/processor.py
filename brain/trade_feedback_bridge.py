class TradeFeedbackBridge:
    """
    Connects execution results
    with learning feedback.
    """

    def __init__(self, reward_engine):
        self.reward = reward_engine


    def process_close(self, symbol, position):

        pnl = position.get(
            "realized_pnl",
            0
        )

        return self.reward.evaluate(
            symbol,
            pnl
        )
