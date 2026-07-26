class AutonomousExecutionMonitoredCommandPipeline:
    """
    Command pipeline with monitoring integration.
    """

    def __init__(
        self,
        pipeline,
        monitor
    ):

        self.pipeline = pipeline
        self.monitor = monitor


    def execute(
        self,
        source,
        command
    ):

        result = self.pipeline.execute(
            source,
            command
        )

        self.monitor.record(
            result
        )

        return result
