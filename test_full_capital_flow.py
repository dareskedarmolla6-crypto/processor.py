from brain.capital_allocator import CapitalAllocator
from brain.portfolio_manager import PortfolioManager
from brain.position_manager import PositionManager
from brain.execution_engine import ExecutionEngine
from brain.smart_exit import SmartExit
from brain.risk_engine import RiskEngine
from risk.risk_manager import RiskGovernor


class MockStore:

    def __init__(self):
        self.data = {
            "system_status": "RUN"
        }

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)


def run_full_capital_flow():

    print("========== FULL CAPITAL FLOW TEST ==========")


    # =========================
    # SETUP
    # =========================

    balance = 1000


    allocator = CapitalAllocator(
        max_single_asset=0.20,
        max_total_exposure=0.50
    )


    portfolio = PortfolioManager(
        max_positions=5,
        max_exposure=0.50
    )


    execution = ExecutionEngine()
    smart_exit = SmartExit()

    risk = RiskEngine(
        max_risk_per_trade=0.03
    )


    position_manager = PositionManager(
        execution=execution,
        smart_exit=smart_exit,
        risk_engine=risk
    )


    store = MockStore()

    governor = RiskGovernor(
        store
    )


    # =========================
    # TEST 1
    # CAPITAL ALLOCATION
    # =========================

    opportunities = [

        {
            "symbol": "BTCUSDT",
            "confidence": 1.0
        },

        {
            "symbol": "ETHUSDT",
            "confidence": 0.5
        },

        {
            "symbol": "SOLUSDT",
            "confidence": 0.8
        }

    ]


    allocations = allocator.allocate(
        balance,
        opportunities
    )


    print("\nALLOCATIONS:")
    print(allocations)


    assert allocations["BTCUSDT"] == 200



    # =========================
    # TEST 2
    # GOVERNOR CHECK
    # =========================

    status = governor.approve_trade()

    print(
        "\nGOVERNOR:",
        status
    )


    assert status[0] is True



    # =========================
    # TEST 3
    # PORTFOLIO APPROVAL
    # =========================

    for symbol, amount in allocations.items():

        approval = portfolio.approve_new_position(
            balance,
            execution.positions,
            amount
        )


        print(
            symbol,
            "PORTFOLIO:",
            approval
        )


        if approval == "APPROVED":

            result = position_manager.manage(
                symbol,
                {
                    "signal": "BUY"
                },
                price=100,
                balance=balance,
                stop_loss_price=98
            )


            print(
                "TRADE:",
                result
            )


            assert result["action"] == "OPEN"



    # =========================
    # FINAL STATE
    # =========================

    print(
        "\nFINAL POSITIONS:"
    )

    print(
        execution.positions
    )


    assert len(execution.positions) > 0


    print(
        "\nFULL CAPITAL FLOW TEST PASSED ✅"
    )



if __name__ == "__main__":
    run_full_capital_flow()
