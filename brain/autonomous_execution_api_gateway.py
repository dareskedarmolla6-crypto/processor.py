class AutonomousExecutionAPIGateway:
    """
    External control gateway for autonomous execution system.
    """

    def __init__(
        self,
        controller
    ):

        self.controller = controller


    def start(self):

        return self.controller.start()


    def stop(self):

        return self.controller.stop()


    def status(self):

        return self.controller.status()
