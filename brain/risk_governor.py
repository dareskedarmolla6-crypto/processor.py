class RiskGovernor:
    """
    Autonomous Risk Governor V8.1

    Controls:
    - Capital permission
    - Weak asset blocking
    - Exposure control
    - Dynamic risk adaptation
    """


    def __init__(self, risk_engine=None, risk_adapter=None):

        self.risk_engine = risk_engine
        self.risk_adapter = risk_adapter



    def approve(
        self,
        symbol,
        allocation,
        status,
        balance,
        open_positions=[]
    ):


        # Current dynamic risk
        current_risk = 0.03

        if self.risk_adapter:

            current_risk = self.risk_adapter.get_risk()



        if allocation <= 0:

            return {
                "symbol": symbol,
                "decision": "BLOCK",
                "reason": "NO_CAPITAL",
                "risk": current_risk
            }



        if status == "WEAK":

            return {
                "symbol": symbol,
                "decision": "BLOCK",
                "reason": "WEAK_ASSET",
                "risk": current_risk
            }



        if self.risk_engine:

            result = self.risk_engine.check_trade(
                balance,
                allocation,
                open_positions
            )


            if result != "APPROVED":

                return {
                    "symbol": symbol,
                    "decision": "BLOCK",
                    "reason": result,
                    "risk": current_risk
                }



        return {
            "symbol": symbol,
            "decision": "APPROVED",
            "allocation": allocation,
            "risk": current_risk
        }
