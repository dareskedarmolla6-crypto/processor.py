import json
import os


class RiskMemory:
    """
    FSE Risk Memory V8.6

    Persistent storage for dynamic risk.
    """

    def __init__(self, path="risk_memory.json"):

        self.path = path


    def save(self, risk):

        data = {
            "risk": risk
        }

        with open(
            self.path,
            "w"
        ) as f:

            json.dump(
                data,
                f
            )


    def load(self, default=0.03):

        if not os.path.exists(self.path):

            return default


        with open(
            self.path,
            "r"
        ) as f:

            data = json.load(f)


        return data.get(
            "risk",
            default
        )
