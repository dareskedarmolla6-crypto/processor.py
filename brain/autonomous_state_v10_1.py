import json
import os


class AutonomousStateV10_1:
    """
    FSE Autonomous Persistent State V10.1

    Stores:
    - Cycle state
    - Portfolio state
    - Memory state
    - Recovery information
    """


    def __init__(
        self,
        path="autonomous_state_v10_1.json"
    ):

        self.path = path

        self.state = {
            "cycles": 0,
            "status": "READY",
            "portfolio": [],
            "memory": {}
        }

        self.load()



    # -------------------------
    # LOAD STATE
    # -------------------------

    def load(self):

        if os.path.exists(self.path):

            with open(
                self.path,
                "r"
            ) as f:

                self.state = json.load(f)



    # -------------------------
    # SAVE STATE
    # -------------------------

    def save(self):

        with open(
            self.path,
            "w"
        ) as f:

            json.dump(
                self.state,
                f,
                indent=4
            )



    # -------------------------
    # UPDATE
    # -------------------------

    def update(
        self,
        state
    ):

        self.state = state

        self.save()



    # -------------------------
    # RECOVERY
    # -------------------------

    def recover(self):

        return self.state



    def get(self):

        return self.state
