from brain.execution_engine import ExecutionEngine


def test_execution_engine_opens_buy_position():

    engine = ExecutionEngine()

    position = engine.open(
        symbol="BTCUSDT",
        side="LONG",
        size=1.0,
        price=60000
    )

    assert position["status"] == "OPEN"
    assert position["symbol"] == "BTCUSDT"
    assert position["side"] == "LONG"

    assert "BTCUSDT" in engine.positions
    assert len(engine.positions["BTCUSDT"]) == 1


def test_execution_engine_rejects_invalid_price():

    engine = ExecutionEngine()

    result = engine.open(
        symbol="BTCUSDT",
        side="LONG",
        size=1,
        price=0
    )

    assert result == "INVALID_PARAMS"
