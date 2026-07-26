class AutonomousExecutionCommandPipeline:
    """
    Unified command execution pipeline.
    """

    def __init__(
        self,
        validator,
        router
    ):

        self.validator = validator
        self.router = router



    def execute(
        self,
        command
    ):

        if not self.validator.validate(command):

            return {
                "error": "INVALID_COMMAND"
            }


        return self.router.execute(command)
