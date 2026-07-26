class AutonomousExecutionRecoveryPersistenceCycle:
    """
    Execution state persistence and recovery coordinator.
    """


    def __init__(
        self,
        state_store,
        persistence
    ):

        self.state_store = state_store
        self.persistence = persistence



    def save_state(self):

        state = self.state_store.snapshot()

        return self.persistence.save(
            state
        )



    def restore_state(self):

        state = self.persistence.load()

        if not state:
            return False

        self.state_store.restore(
            state
        )

        return True
