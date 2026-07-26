import json
import os


class StateStorage:
    """
    FSE Autonomous State Storage V10.10

    Responsible for:
    - Saving brain state
    - Loading previous state
    - Recovery after restart
    """

    def __init__(self, filename="autonomous_state.json"):
        self.filename = filename


    def save(self, state):

        with open(
            self.filename,
            "w"
        ) as file:

            json.dump(
                state,
                file,
                indent=4
            )

        return {
            "status": "SAVED"
        }


    def load(self):

        if not os.path.exists(self.filename):

            return {
                "status": "EMPTY",
                "state": {}
            }


        with open(
            self.filename,
            "r"
        ) as file:

            state = json.load(file)


        return {
            "status": "LOADED",
            "state": state
        }
