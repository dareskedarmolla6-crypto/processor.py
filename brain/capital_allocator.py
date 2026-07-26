class CapitalAllocator:
    """
    Production Capital Allocation Engine

    Responsibilities:
    - Allocate real available capital
    - Use validated market opportunities
    - No hardcoded symbols
    - No artificial capital defaults
    """

    def __init__(self):
        self.cycles = 0


    def allocate(
        self,
        total_capital=None,
        assets=None,
        balance=None,
        opportunities=None
    ):

        self.cycles += 1


        if isinstance(total_capital, dict) and "positions" in total_capital:

            pipeline_data = total_capital

            raw_positions = pipeline_data.get(
                "positions",
                []
            )

            normalized_assets = []

            for pos in raw_positions:

                if isinstance(pos, dict):
                    normalized_assets.append(pos)


            assets = normalized_assets


            if balance is not None:
                total_capital = balance
            else:
                total_capital = pipeline_data.get(
                    "capital"
                )


        if total_capital is None:
            total_capital = balance


        if assets is None:
            assets = opportunities


        allocations = []


        if not assets or total_capital is None:
            return allocations



        total_score = 0


        for item in assets:

            score = item.get(
                "score",
                item.get(
                    "confidence",
                    0
                )
            )


            if score < 0:
                score = 0


            total_score += score



        for item in assets:

            symbol = item.get(
                "symbol"
            )


            if not symbol:
                continue


            score = item.get(
                "score",
                item.get(
                    "confidence",
                    0
                )
            )


            if total_score > 0:

                amount = (
                    score /
                    total_score
                ) * total_capital


            else:

                amount = (
                    total_capital /
                    len(assets)
                )


            allocations.append(
                {
                    "symbol": symbol,
                    "allocation": round(
                        amount,
                        2
                    ),
                    "score": score
                }
            )


        return allocations



    def state(self):

        return {
            "cycles": self.cycles
        }
