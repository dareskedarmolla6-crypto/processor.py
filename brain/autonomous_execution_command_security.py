class AutonomousExecutionCommandSecurity:
    """
    Security layer for autonomous execution commands.
    """

    def __init__(
        self,
        allowed_sources=None
    ):

        self.allowed_sources = allowed_sources or [
            "system"
        ]


    def authorize(
        self,
        source
    ):

        return source in self.allowed_sources
