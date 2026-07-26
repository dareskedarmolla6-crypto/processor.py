from datetime import datetime, UTC


class AdaptiveLearningEngineV10_64:
    """
    FSE Adaptive Learning Engine V10.64

    Responsibilities
    ----------------
    - Consume real trade rewards
    - Update learning state
    - Track strategy performance trend
    - Produce learning adjustment record

    Does NOT contain
    ----------------
    - Fake training data
    - Simulated trades
    - Random decisions
    """


    def __init__(self):

        self.learning_state = {
            "total_feedback": 0,
            "positive_rewards": 0,
            "negative_rewards": 0,
            "last_reward": 0.0,
            "performance_bias": 0.0
        }



    def learn(
        self,
        reward_record: dict
    ) -> dict:


        if not reward_record:
            raise ValueError(
                "Reward record required"
            )


        reward = reward_record.get(
            "reward"
        )


        if reward is None:
            raise ValueError(
                "Reward value missing"
            )


        self.learning_state["total_feedback"] += 1


        if reward > 0:
            self.learning_state["positive_rewards"] += 1

        elif reward < 0:
            self.learning_state["negative_rewards"] += 1


        self.learning_state["last_reward"] = reward


        total = self.learning_state["total_feedback"]


        self.learning_state["performance_bias"] = (
            (
                self.learning_state["positive_rewards"]
                -
                self.learning_state["negative_rewards"]
            )
            /
            total
        )


        return {
            "symbol": reward_record["symbol"],
            "position_id": reward_record["position_id"],
            "learning_state": self.learning_state.copy(),
            "updated_at": datetime.now(
                UTC
            ).isoformat()
        }
