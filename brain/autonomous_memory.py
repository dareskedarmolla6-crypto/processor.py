import json
import os
from datetime import datetime


class AutonomousMemory:
    """
    FSE Autonomous Unified Memory V8.7

    Stores:
    - Portfolio state
    - Risk state
    - Learning cycles
    """

    def __init__(
        self,
        path="autonomous_memory.json"
    ):

        self.path = path

        self.data = {
            "portfolio": {},
            "risk": 0.03,
            "history": []
        }

        self.load()


    # -------------------------
    # LOAD
    # -------------------------
    def load(self):

        if os.path.exists(self.path):

            with open(self.path, "r") as f:

                self.data = json.load(f)


    # -------------------------
    # SAVE
    # -------------------------
    def save(self):

        with open(self.path, "w") as f:

            json.dump(
                self.data,
                f,
                indent=4
            )


    # -------------------------
    # PORTFOLIO
    # -------------------------
    def update_portfolio(
        self,
        portfolio
    ):

        self.data["portfolio"] = portfolio

        self.save()


    # -------------------------
    # RISK
    # -------------------------
    def update_risk(
        self,
        risk
    ):

        self.data["risk"] = risk

        self.save()


    # -------------------------
    # CYCLE MEMORY
    # -------------------------
    def record_cycle(
        self,
        result
    ):

        self.data["history"].append(
            {
                "time": str(datetime.now()),
                "result": result
            }
        )

        self.save()


    def get(self):

        return self.data
