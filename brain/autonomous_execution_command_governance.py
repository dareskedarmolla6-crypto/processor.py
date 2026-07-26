class AutonomousExecutionCommandGovernance:
    """
    Governance layer for execution commands.
    """

    def __init__(
        self,
        policies=None
    ):

        self.policies = policies or {
            "start": True,
            "stop": True,
            "status": True
        }


    def allowed(
        self,
        command
    ):

        return self.policies.get(
            command,
            False
        )
