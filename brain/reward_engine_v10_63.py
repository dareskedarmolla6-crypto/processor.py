from datetime import datetime, UTC


class RewardEngineV10_63:
    """
    FSE Production Reward Engine V10.63

    Responsibilities
    ----------------
    - Convert trade feedback into learning reward
    - Produce normalized reward signal
    - Provide learning metadata

    Does NOT contain:
    - Strategy logic
    - Market prediction
    - Fake rewards
    """

    def calculate(
        self,
        feedback: dict
    ) -> dict:

        if not feedback:
            raise ValueError(
                "Feedback required"
            )


        outcome = feedback["outcome"]

        pnl = feedback["realized_pnl"]


        if outcome == "WIN":
            reward = 1.0

        elif outcome == "LOSS":
            reward = -1.0

        else:
            reward = 0.0


        return {
            "position_id": feedback["position_id"],
            "symbol": feedback["symbol"],
            "reward": reward,
            "realized_pnl": pnl,
            "outcome": outcome,
            "generated_at": datetime.now(
                UTC
            ).isoformat()
        }
