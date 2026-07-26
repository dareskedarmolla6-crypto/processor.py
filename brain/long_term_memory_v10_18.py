import json
import os
from datetime import datetime


class LongTermMemoryV10_18:
    """
    FSE Long Term Memory Engine V10.18

    Persistent learning storage
    """

    def __init__(
        self,
        file_path="brain_memory.json"
    ):

        self.file_path = file_path

        self.state = {
            "history": {},
            "learning": {},
            "last_update": None
        }

        self.load()


    # -------------------------
    # SAVE MEMORY
    # -------------------------
    def save(self):

        self.state["last_update"] = str(
            datetime.now()
        )

        with open(
            self.file_path,
            "w"
        ) as f:

            json.dump(
                self.state,
                f,
                indent=4
            )


        return {
            "status": "SAVED"
        }



    # -------------------------
    # LOAD MEMORY
    # -------------------------
    def load(self):

        if os.path.exists(
            self.file_path
        ):

            with open(
                self.file_path,
                "r"
            ) as f:

                self.state = json.load(
                    f
                )



    # -------------------------
    # STORE RESULT
    # -------------------------
    def remember(
        self,
        symbol,
        result
    ):

        if symbol not in self.state["history"]:

            self.state["history"][symbol] = []


        self.state["history"][symbol].append(
            result
        )


        self.save()


        return {
            "status": "REMEMBERED",
            "symbol": symbol
        }



    # -------------------------
    # GET KNOWLEDGE
    # -------------------------
    def get_memory(self):

        return self.state
