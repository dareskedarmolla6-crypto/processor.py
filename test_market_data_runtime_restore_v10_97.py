from market.market_data_runtime import MarketDataRuntime


class StubScheduler:

    def run_once(self, symbols):
        pass


class MemoryRepository:

    def __init__(self):
        self.state = None

    def save_state(self, state):
        self.state = state.copy()

    def load_state(self):
        return self.state


def test_runtime_restores_previous_state():

    repo = MemoryRepository()

    # የቆየ የፕሮዳክሽን ሁኔታን ማስመስል (cycles = 25, status = RUNNING)
    repo.save_state({
        "status": "RUNNING",
        "cycles": 25,
        "last_error": None
    })

    runtime = MarketDataRuntime(
        StubScheduler(),
        state_repository=repo
    )

    state = runtime.state()

    # ማረጋገጫ — cycles መመለስ አለበት፣ ነገር ግን status በደህንነት መርህ STOPPED መሆን አለበት
    assert state["cycles"] == 25
    assert state["status"] == "STOPPED"


def test_runtime_can_start_after_restore():

    repo = MemoryRepository()

    repo.save_state({
        "status": "RUNNING",
        "cycles": 10,
        "last_error": None
    })

    runtime = MarketDataRuntime(
        StubScheduler(),
        state_repository=repo
    )

    # ሪስቶር ከተደረገ በኋላ ሲስተሙ በሰላም መነሳት መቻሉን መፈተሽ
    runtime.start()

    assert runtime.running is True
    assert runtime.state()["status"] == "RUNNING"
