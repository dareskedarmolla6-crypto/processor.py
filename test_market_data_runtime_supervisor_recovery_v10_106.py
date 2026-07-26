from market.market_data_runtime_supervisor import (
    MarketDataRuntimeSupervisor
)


class UnhealthyRuntime:

    def __init__(self):
        self._running = False
        self.restart_called = False


    def restart(self):

        self._running = True
        self.restart_called = True

        return {
            "status": "RUNNING"
        }


    def health(self):

        if self.restart_called:
            return {
                "status": "RUNNING",
                "healthy": True
            }

        return {
            "status": "ERROR",
            "healthy": False
        }


    @property
    def running(self):
        return self._running



class HealthyRuntime:

    @property
    def running(self):
        return True


    def health(self):

        return {
            "status": "RUNNING",
            "healthy": True
        }



def test_recovery_restarts_unhealthy_runtime():

    runtime = UnhealthyRuntime()

    supervisor = MarketDataRuntimeSupervisor(
        runtime
    )

    result = supervisor.recover()

    assert result["recovered"] is True
    assert runtime.restart_called is True



def test_recovery_skips_healthy_runtime():

    runtime = HealthyRuntime()

    supervisor = MarketDataRuntimeSupervisor(
        runtime
    )

    result = supervisor.recover()

    assert result["recovered"] is False
    assert result["reason"] == "runtime_healthy"
