class AutonomousExecutionGovernedCommandPipeline:
    """
    Command pipeline with security, governance,
    validation and audit control.
    """

    def __init__(
        self,
        security,
        governance,
        validator,
        router,
        audit
    ):

        self.security = security
        self.governance = governance
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

            self.audit.record(command, result)

            return result


        if not self.governance.allowed(command):

            result = {
                "error": "COMMAND_NOT_ALLOWED"
            }

            self.audit.record(command, result)

            return result


        if not self.validator.validate(command):

            result = {
                "error": "INVALID_COMMAND"
            }

            self.audit.record(command, result)

            return result


        result = self.router.execute(command)

        self.audit.record(
            command,
            result
        )

        return result
