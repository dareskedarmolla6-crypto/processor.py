from brain.position_manager import PositionManager
from brain.execution_engine import ExecutionEngine
from brain.smart_exit import SmartExit
from brain.risk_engine import RiskEngine


def run_dynamic_symbols_test():

    print("========== DYNAMIC SYMBOL TEST ==========")


    # =========================
    # SETUP
    # =========================

    execution = ExecutionEngine()
    smart_exit = SmartExit()
    risk = RiskEngine(
        max_risk_per_trade=0.03
    )

    pm = PositionManager(
        execution=execution,
        smart_exit=smart_exit,
        risk_engine=risk
    )


    balance = 1000


    # =========================
    # SYMBOL LIST
    # =========================

    symbols = [
        {
            "symbol": "BTCUSDT",
            "signal": "BUY",
            "price": 100
        },
        {
            "symbol": "ETHUSDT",
            "signal": "BUY",
            "price": 200
        },
        {
            "symbol": "SOLUSDT",
            "signal": "SELL",
            "price": 50
        },
        {
            "symbol": "BNBUSDT",
            "signal": "BUY",
            "price": 300
        }
    ]


    # =========================
    # OPEN POSITIONS
    # =========================

    for item in symbols:

        stop_loss = (
            item["price"] * 0.98
            if item["signal"] == "BUY"
            else item["price"] * 1.02
        )

        result = pm.manage(
            item["symbol"],
            {
                "signal": item["signal"]
            },
            price=item["price"],
            balance=balance,
            stop_loss_price=stop_loss
        )


        print(
            "\n",
            item["symbol"],
            ":",
            result
        )


        assert result["action"] == "OPEN"



    # =========================
    # VERIFY PORTFOLIO
    # =========================

    print("\nOPEN POSITIONS:")
    print(execution.positions)


    assert len(execution.positions) == 4


    assert "BTCUSDT" in execution.positions
    assert "ETHUSDT" in execution.positions
    assert "SOLUSDT" in execution.positions
    assert "BNBUSDT" in execution.positions


    print(
        "\nDYNAMIC SYMBOL TEST PASSED ✅"
    )


if __name__ == "__main__":
    run_dynamic_symbols_test()
