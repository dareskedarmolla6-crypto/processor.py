class AutonomousExecutionSecureCommandPipeline:
    """
    Secure command execution pipeline.
    """

    def __init__(
        self,
        security,
        validator,
        router,
        audit
    ):

        self.security = security
        self.validator = validator
        self.router = router
        self.audit = audit



    def execute(
        self,
        source,
        command
    ):

        if not self.security.authorize(source):

            result = {
                "error": "UNAUTHORIZED_SOURCE"
            }

            self.audit.record(
                command,
                result
            )

            return result


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
