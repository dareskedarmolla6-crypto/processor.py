class IntelligenceRuntimeStateCoordinatorV10_81:
    """
    FSE Intelligence Runtime State Coordinator V10.81

    Responsibilities
    ----------------
    - Coordinate runtime intelligence state
    - Load current state
    - Update state after recovery

    Does NOT contain
    ----------------
    - Learning logic
    - Decision logic
    - Execution logic
    """


    def __init__(
        self,
        state_store,
        recovery_supervisor
    ):

        self.state_store = state_store
        self.recovery_supervisor = recovery_supervisor



    def get_state(self):

        return self.state_store.load()



    def recover_state(self):

        recovery = (
            self.recovery_supervisor.recover()
        )


        if recovery["status"] != "RECOVERY_READY":

            return {
                "status": "RECOVERY_FAILED",
                "state": None
            }


        return {
            "status": "STATE_RECOVERED",
            "state": recovery["recovery"]
        }



    def save_state(
        self,
        state
    ):

        return self.state_store.save(
            state
        )
