class FeedbackEngine:
    """
    FSE Feedback Learning Engine

    Responsibilities:
    - Receive closed trade results
    - Calculate performance
    - Update Performance Memory
    - Feed Adaptive Brain
    """

    def __init__(self, performance_memory):

        self.memory = performance_memory


    # -------------------------
    # Process Trade Result
    # -------------------------
    def process_result(
        self,
        symbol,
        pnl
    ):

        # Save result into memory
        self.memory.record(
            symbol,
            pnl
        )


        # Calculate updated score
        score = self.memory.score(
            symbol
        )


        status = "WIN"

        if pnl < 0:
            status = "LOSS"


        return {
            "symbol": symbol,
            "pnl": pnl,
            "status": status,
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

            result = self.process_result(
                trade["symbol"],
                trade["pnl"]
            )

            results.append(result)


        return results
