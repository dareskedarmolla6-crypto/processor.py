class PositionSizingEngine:
    """
    FSE Production Position Sizing Engine V10.54

    Responsibilities:
    - Calculate position size from capital
    - Apply risk percentage
    - Prevent invalid allocations

    Does NOT contain:
    - Trading decisions
    - Market prediction
    - Execution logic
    """


    def __init__(
        self,
        max_risk_percent=0.02
    ):

        self.max_risk_percent = max_risk_percent


    def calculate(
        self,
        capital: float,
        price: float,
        risk_percent: float | None = None
    ):

        if capital <= 0:
            raise ValueError(
                "Capital must be positive"
            )

        if price <= 0:
            raise ValueError(
                "Price must be positive"
            )


        risk = (
            risk_percent
            if risk_percent is not None
            else self.max_risk_percent
        )


        if risk <= 0 or risk > 1:
            raise ValueError(
                "Invalid risk percentage"
            )


        risk_amount = (
            capital * risk
        )


        size = (
            risk_amount / price
        )


        return {
            "capital": capital,
            "risk_percent": risk,
            "risk_amount": risk_amount,
            "price": price,
            "size": size
        }
