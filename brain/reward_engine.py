class RewardEngine:
    """
    FSE Reward Engine

    Responsibilities:
    - Evaluate closed trades
    - Calculate reward / penalty
    - Update Performance Memory
    - Feed learning system
    """

    def __init__(self, performance_memory):

        self.memory = performance_memory


    # -------------------------
    # Single Trade Feedback
    # -------------------------
    def evaluate(
        self,
        symbol,
        pnl
    ):

        if pnl > 0:

            status = "WIN"
            reward = pnl

        else:

            status = "LOSS"
            reward = pnl


        # send feedback to memory
        self.memory.record(
            symbol,
            pnl
        )


        score = self.memory.score(
            symbol
        )


        return {
            "symbol": symbol,
            "pnl": pnl,
            "status": status,
            "reward": reward,
            "score": score
        }



    # -------------------------
    # Batch Feedback
    # -------------------------
    def process_batch(
        self,
        trades
    ):

        results = []


        for trade in trades:

            result = self.evaluate(
                trade["symbol"],
                trade["pnl"]
            )

            results.append(
                result
            )


        return results
