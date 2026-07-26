class PortfolioAllocatorV9_4:
    """
    FSE Portfolio Risk Allocator V9.4

    Allocates capital based on:
    - Confidence
    - Risk control
    - Portfolio limits
    """

    def __init__(
        self,
        total_capital=1000,
        max_allocation=0.6
    ):

        self.total_capital = total_capital
        self.max_allocation = max_allocation


    # -------------------------
    # Allocation
    # -------------------------

    def allocate(
        self,
        decisions
    ):

        allocations = []

        total_confidence = sum(
            x["confidence"]
            for x in decisions
            if x["decision"] == "TRADE"
        )


        if total_confidence == 0:

            return []


        for item in decisions:

            if item["decision"] != "TRADE":
                continue


            weight = (
                item["confidence"]
                /
                total_confidence
            )


            amount = (
                self.total_capital
                *
                weight
            )


            # Risk limit
            max_amount = (
                self.total_capital
                *
                self.max_allocation
            )


            amount = min(
                amount,
                max_amount
            )


            allocations.append(
                {
                    "symbol": item["symbol"],
                    "confidence": item["confidence"],
                    "allocation": round(
                        amount,
                        2
                    ),
                    "risk_level": item.get(
                        "risk_level",
                        0.03
                    )
                }
            )


        return allocations
