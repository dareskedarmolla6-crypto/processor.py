class DynamicAllocator:
    """
    FSE Dynamic Capital Allocator V7.5.1

    Allocation based on:
    - Brain performance score
    - Asset status
    - Risk adjustment
    - Portfolio balance
    """

    def __init__(self):

        self.min_allocation = 0


    def allocate(self, capital, assets):

        if not assets:
            return []


        allocations = []


        # Calculate total strength
        total_score = 0

        for asset in assets:

            score = asset.get(
                "score",
                0
            )

            if score < 0:
                score = 0

            total_score += score


        for asset in assets:

            symbol = asset["symbol"]

            score = asset.get(
                "score",
                0
            )

            status = asset.get(
                "status",
                "NORMAL"
            )


            # Base allocation

            if total_score > 0:

                amount = (
                    score / total_score
                ) * capital

            else:

                amount = (
                    capital / len(assets)
                )


            action = "HOLD"


            # Adaptive adjustment

            if status == "STRONG":

                amount *= 0.9
                action = "INCREASE"


            elif status == "WEAK":

                amount *= 0.1
                action = "REDUCE"


            else:

                action = "HOLD"


            allocations.append(
                {
                    "symbol": symbol,
                    "allocation": round(amount,2),
                    "action": action,
                    "score": score,
                    "status": status
                }
            )


        return allocations
