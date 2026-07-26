class FeedbackLoop:
    """
    FSE Feedback Learning Loop

    Execution Result
          ↓
    Reward Engine
          ↓
    Memory Manager
          ↓
    Brain Learning
    """

    def __init__(
        self,
        reward_engine,
        memory_manager=None,
        performance_memory=None,
        optimizer=None
    ):

        self.reward_engine = reward_engine

        if memory_manager is not None:
            self.memory = memory_manager
        elif performance_memory is not None:
            self.memory = performance_memory
        else:
            raise ValueError(
                "memory_manager or performance_memory is required"
            )

        self.optimizer = optimizer

    # -------------------------
    # Single Trade Feedback
    # -------------------------
    def process_trade_result(
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

            result = self.process_trade_result(
                trade["symbol"],
                trade["pnl"]
            )

            results.append(result)

        return results

    # -------------------------
    # Brain Update
    # -------------------------
    def learn(self):

        if self.optimizer:
            return self.optimizer.optimize()

        return None
