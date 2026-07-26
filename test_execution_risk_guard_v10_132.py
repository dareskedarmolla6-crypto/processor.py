from brain.execution_risk_guard import ExecutionRiskGuard


class StubRiskEngine:

    def approve(self, symbol, size, price):
        return True


class RejectRiskEngine:

    def approve(self, symbol, size, price):
        return False



def test_risk_guard_allows_valid_execution():

    guard = ExecutionRiskGuard(
        StubRiskEngine()
    )

    result = guard.check(
        symbol="BTCUSDT",
        size=1,
        price=60000
    )

    assert result["approved"] is True
    assert result["symbol"] == "BTCUSDT"



def test_risk_guard_blocks_rejected_execution():

    guard = ExecutionRiskGuard(
        RejectRiskEngine()
    )

    result = guard.check(
        symbol="BTCUSDT",
        size=1,
        price=60000
    )

    assert result["approved"] is False



def test_risk_guard_rejects_invalid_parameters():

    guard = ExecutionRiskGuard(
        StubRiskEngine()
    )

    result = guard.check(
        symbol="BTCUSDT",
        size=0,
        price=60000
    )

    assert result == "INVALID_PARAMS"
