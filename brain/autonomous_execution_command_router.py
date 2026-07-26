class AutonomousExecutionCommandRouter:
    """
    Routes external execution commands.
    """

    def __init__(
        self,
        gateway
    ):

        self.gateway = gateway


    def execute(
        self,
        command
    ):

        if command == "start":
            return self.gateway.start()

        if command == "stop":
            return self.gateway.stop()

        if command == "status":
            return self.gateway.status()

        return {
            "error": "UNKNOWN_COMMAND"
        }
