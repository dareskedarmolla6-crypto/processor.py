class PortfolioIntelligence:
    """
    FSE Portfolio Intelligence V9.2

    Selects the strongest trading opportunities
    from multiple candidate signals.
    """

    def __init__(self, max_positions=3):
        self.max_positions = max_positions

    def rank(self, decisions):

        ranked = sorted(
            decisions,
            key=lambda x: x["confidence"],
            reverse=True
        )

        return ranked

    def select(self, decisions):

        ranked = self.rank(decisions)

        selected = []

        for item in ranked:

            if item["decision"] != "TRADE":
                continue

            selected.append(item)

            if len(selected) >= self.max_positions:
                break

        return selected

    def statistics(self, decisions):

        selected = self.select(decisions)

        return {
            "total_candidates": len(decisions),
            "selected": len(selected),
            "rejected": len(decisions) - len(selected)
        }
