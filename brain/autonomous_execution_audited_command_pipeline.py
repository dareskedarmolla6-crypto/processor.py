class AutonomousExecutionAuditedCommandPipeline:
    """
    Command pipeline with execution audit.
    """

    def __init__(
        self,
        validator,
        router,
        audit
    ):

        self.validator = validator
        self.router = router
        self.audit = audit



    def execute(
        self,
        command
    ):

        if not self.validator.validate(command):

            result = {
                "error": "INVALID_COMMAND"
            }

            self.audit.record(
                command,
                result
            )

            return result


        result = self.router.execute(
            command
        )


        self.audit.record(
            command,
            result
        )


        return result
