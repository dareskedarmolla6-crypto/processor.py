class AutonomousExecutionLifecycleCoordinator:
    """
    Coordinates execution close lifecycle.

    Flow:

    ExecutionEngine
        ↓
    Persistence
        ↓
    Feedback
        ↓
    State Store
    """

    def __init__(
        self,
        execution_engine,
        persistence=None,
        feedback_bridge=None,
        state_store=None
    ):

        self.execution_engine = execution_engine
        self.persistence = persistence
        self.feedback_bridge = feedback_bridge
        self.state_store = state_store

    def close_position(
        self,
        symbol,
        position_id,
        price,
        reason="MANUAL"
    ):

        position = self.execution_engine.close_by_id(
            symbol,
            position_id,
            price,
            reason
        )

        if not isinstance(position, dict):
            return position

        if self.persistence:
            self.persistence.close_position(position)

        if self.feedback_bridge:
            self.feedback_bridge.process(position)

        if self.state_store:
            self.state_store.increment_execution()

        return position
