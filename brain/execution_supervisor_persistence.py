class ExecutionSupervisorPersistence:
    """
    Production integration layer between
    execution supervisor and persistence.

    Responsibilities:
    - Persist opened positions
    - Persist closed positions
    - Restore execution state
    """


    def __init__(
        self,
        persistence
    ):

        self.persistence = persistence



    def save_open_position(
        self,
        position
    ):

        if not position:
            return {
                "status": "REJECTED",
                "reason": "EMPTY_POSITION"
            }


        self.persistence.save_position(
            position
        )


        return {
            "status": "SAVED",
            "position_id": position["id"]
        }



    def save_closed_position(
        self,
        position
    ):

        if not position:
            return {
                "status": "REJECTED",
                "reason": "EMPTY_POSITION"
            }


        self.persistence.close_position(
            position
        )


        return {
            "status": "UPDATED",
            "position_id": position["id"]
        }



    def restore(
        self
    ):

        return self.persistence.restore_positions()
