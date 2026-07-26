class AutonomousExecutionCommandValidator:
    """
    Validates autonomous execution commands.
    """

    ALLOWED_COMMANDS = {
        "start",
        "stop",
        "status"
    }


    def validate(
        self,
        command
    ):

        if command in self.ALLOWED_COMMANDS:

            return True

        return False
