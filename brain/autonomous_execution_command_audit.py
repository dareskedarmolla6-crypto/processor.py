class AutonomousExecutionCommandAudit:
    """
    Records autonomous execution commands.
    """

    def __init__(self):

        self.history = []


    def record(
        self,
        command,
        result
    ):

        event = {
            "command": command,
            "result": result
        }

        self.history.append(event)

        return event



    def get_history(self):

        return list(self.history)
