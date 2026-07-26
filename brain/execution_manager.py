class ExecutionManager:
    """
    Autonomous Execution Layer V6
    """

    def __init__(self, position_manager):
        self.position_manager = position_manager
        self.executed = []
        # Added missing attributes for PositionManager compatibility
        self.positions = {}
        self.position_id = 0

    def execute(
        self,
        decision,
        risk_result,
        size=1,
        entry=50
    ):

        symbol = decision["symbol"]

        if decision["decision"] != "TRADE":
            return {
                "status": "SKIPPED",
                "reason": "NO_TRADE_SIGNAL",
                "symbol": symbol
            }

        if risk_result["decision"] != "APPROVED":
            return {
                "status": "BLOCKED",
                "reason": risk_result.get(
                    "reason",
                    "RISK_BLOCK"
                ),
                "symbol": symbol
            }

        # Positioning logic
        position = self.position_manager.manage(
            symbol,
            {
                "signal": "BUY"
            },
            entry
        )

        result = {
            "status": "EXECUTED",
            "symbol": symbol,
            "position": position
        }

        self.executed.append(result)

        return result

    def open(self, symbol, side, size, price):
        """
        Creates a new position and registers it in the manager.
        This fixes the AttributeError: 'ExecutionManager' object has no attribute 'open'
        """
        self.position_id += 1
        
        position = {
            "id": self.position_id,
            "symbol": symbol,
            "side": side,
            "size": size,
            "entry_price": price,
            "status": "OPEN"
        }
        
        # Register position
        if symbol not in self.positions:
            self.positions[symbol] = []
        
        self.positions[symbol].append(position)
        
        return position
