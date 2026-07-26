class ExecutionFeedbackBridge:
    """
    Connects execution results with learning memory.

    Flow
    ----
    ExecutionEngine
          ↓
    Feedback Bridge
          ↓
    PerformanceMemory
    """

    def __init__(self, memory):
        self._memory = memory


    def process(self, execution_result):

        if not execution_result:
            return "INVALID_EXECUTION_RESULT"


        if execution_result.get("status") != "CLOSED":
            return "INVALID_EXECUTION_RESULT"


        symbol = execution_result.get(
            "symbol"
        )

        pnl = execution_result.get(
            "realized_pnl",
            0
        )


        if not symbol:
            return "INVALID_EXECUTION_RESULT"


        self._memory.record(
            symbol,
            pnl
        )


        status = (
            "WIN"
            if pnl > 0
            else "LOSS"
        )


        return {
            "symbol": symbol,
            "pnl": pnl,
            "status": status
        }
