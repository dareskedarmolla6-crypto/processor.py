class PortfolioRebalancer:
    """
    FSE Autonomous Portfolio Rebalance V7.4

    Uses:
    - Brain performance report
    - Asset strength
    - Risk adjustment
    """

    def __init__(self):
        self.min_allocation = 0


    def rebalance(self, capital, report):

        allocations = []

        if not report:
            return allocations


        strong = []
        weak = []
        normal = []


        for symbol, data in report.items():

            status = data.get(
                "status",
                "NORMAL"
            )

            if status == "STRONG":
                strong.append(symbol)

            elif status == "WEAK":
                weak.append(symbol)

            else:
                normal.append(symbol)


        strong_capital = capital * 0.9
        weak_capital = capital * 0.05
        normal_capital = capital * 0.05


        for symbol in strong:

            allocations.append({
                "symbol": symbol,
                "allocation": round(
                    strong_capital / len(strong),
                    2
                ),
                "action": "INCREASE"
            })


        for symbol in weak:

            allocations.append({
                "symbol": symbol,
                "allocation": round(
                    weak_capital / len(weak),
                    2
                ),
                "action": "REDUCE"
            })


        for symbol in normal:

            allocations.append({
                "symbol": symbol,
                "allocation": round(
                    normal_capital / len(normal),
                    2
                ),
                "action": "HOLD"
            })


        return allocations
