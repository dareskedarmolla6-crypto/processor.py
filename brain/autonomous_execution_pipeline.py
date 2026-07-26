class AutonomousExecutionPipeline:
    """
    Autonomous Execution Pipeline

    Flow:

    Decision
        |
        v
    Risk Guard
        |
        v
    Execution Engine
    """

    def __init__(
        self,
        execution_engine,
        risk_guard
    ):
        self._execution = execution_engine
        self._risk_guard = risk_guard


    def execute(
        self,
        symbol,
        side,
        size,
        price
    ):

        risk_result = self._risk_guard.check(
            symbol,
            size,
            price
        )


        if risk_result == "INVALID_PARAMS":
            return "INVALID_PARAMS"


        if not risk_result["approved"]:
            return risk_result


        position = self._execution.open(
            symbol,
            side,
            size,
            price
        )


        return position
