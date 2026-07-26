class AutonomousExecutionSystemController:
    """
    Main control interface for autonomous execution system.
    """

    def __init__(
        self,
        bootstrap
    ):

        self.bootstrap = bootstrap



    def start(self):

        return self.bootstrap.start()



    def stop(self):

        return self.bootstrap.stop()



    def status(self):

        return self.bootstrap.status()
