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



# =========================
# MOCK MARKET FEED
# =========================

def market_feed():

    return [

        {
            "symbol": "BTCUSDT",
            "price": 60000,
            "signal": "BUY",
            "confidence": 0.95
        },

        {
            "symbol": "ETHUSDT",
            "price": 3000,
            "signal": "BUY",
            "confidence": 0.85
        },

        {
            "symbol": "SOLUSDT",
            "price": 150,
            "signal": "SELL",
            "confidence": 0.75
        }

    ]



def run_autonomous_brain_loop():

    print("========== AUTONOMOUS BRAIN LOOP TEST ==========")


    balance = 1000


    # =========================
    # INIT BRAIN
    # =========================

    allocator = CapitalAllocator()

    portfolio = PortfolioManager()

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
    # MARKET SCAN
    # =========================

    opportunities = market_feed()


    print("\nMARKET OPPORTUNITIES:")
    print(opportunities)



    # =========================
    # CONFIDENCE FILTER
    # =========================

    filtered = []

    for item in opportunities:

        if item["confidence"] >= 0.70:
            filtered.append(item)


    print("\nFILTERED SIGNALS:")
    print(filtered)



    # =========================
    # CAPITAL ALLOCATION
    # =========================

    allocation_input = []

    for item in filtered:

        allocation_input.append(
            {
                "symbol": item["symbol"],
                "confidence": item["confidence"]
            }
        )


    allocations = allocator.allocate(
        balance,
        allocation_input
    )


    print("\nALLOCATIONS:")
    print(allocations)



    # =========================
    # GOVERNOR
    # =========================

    status = governor.approve_trade()

    print(
        "\nRISK GOVERNOR:",
        status
    )

    assert status[0] is True



    # =========================
    # EXECUTION LOOP
    # =========================

    for item in filtered:


        symbol = item["symbol"]


        approval = portfolio.approve_new_position(
            balance,
            execution.positions,
            allocations[symbol]
        )


        print(
            "\nPORTFOLIO CHECK:",
            symbol,
            approval
        )


        if approval == "APPROVED":


            stop_loss = (
                item["price"] * 0.98
                if item["signal"] == "BUY"
                else item["price"] * 1.02
            )


            result = position_manager.manage(

                symbol,

                {
                    "signal": item["signal"]
                },

                price=item["price"],

                balance=balance,

                stop_loss_price=stop_loss

            )


            print(
                "EXECUTION:",
                result
            )


            assert result["action"] == "OPEN"



    # =========================
    # FINAL MEMORY
    # =========================

    print(
        "\nFINAL PORTFOLIO:"
    )

    print(
        execution.positions
    )


    assert len(execution.positions) > 0


    print(
        "\nAUTONOMOUS BRAIN LOOP PASSED ✅"
    )



if __name__ == "__main__":
    run_autonomous_brain_loop()
