class ClosedTradeHandler:
    """
    CLOSED TRADE LEARNING BRIDGE

    Flow:
    ExecutionEngine
          ↓
    ClosedTradeHandler
          ↓
    RewardEngine
          ↓
    Memory
    """

    def __init__(self, reward_engine):
        self.reward = reward_engine

    def process_closed_position(self, position):

        if position.get("status") != "CLOSED":
            return {
                "status": "IGNORED",
                "reason": "POSITION_NOT_CLOSED"
            }

        # ከ ExecutionEngine የተላከውን symbol እንጠቀማለን
        symbol = position.get("symbol", "UNKNOWN")
        pnl = position.get("realized_pnl", 0)

        # Reward Engine ለትምህርት (Learning) እንዲጠቀምበት ይላካል
        result = self.reward.evaluate(
            symbol,
            pnl
        )

        return {
            "status": "LEARNED",
            "trade": position,
            "reward_result": result
        }
