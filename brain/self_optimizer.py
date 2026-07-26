class SelfOptimizer:
    """
    FSE Self Optimizer

    - Analyze performance
    - Adjust confidence threshold
    - Adjust risk level
    """


    def __init__(
        self,
        performance_memory,
        base_confidence=0.75,
        base_risk=0.03
    ):

        self.memory = performance_memory

        self.confidence_threshold = base_confidence
        self.risk_level = base_risk



    # -------------------------
    # Analyze Performance
    # -------------------------
    def analyze(self):

        report = {}

        for symbol, data in self.memory.history.items():

            score = self.memory.score(symbol)


            if score >= 80:
                status = "STRONG"

            elif score >= 50:
                status = "NORMAL"

            else:
                status = "WEAK"


            report[symbol] = {
                "score": score,
                "status": status,
                "trades": data["trades"],
                "pnl": data["pnl"]
            }


        return report



    # -------------------------
    # Optimize Parameters
    # -------------------------
    def optimize(self):

        report = self.analyze()


        strong = 0
        weak = 0


        for item in report.values():

            if item["status"] == "STRONG":
                strong += 1


            if item["status"] == "WEAK":
                weak += 1



        if strong >= weak and strong > 0:

            self.confidence_threshold = 0.70
            self.risk_level = 0.04


        elif weak > strong:

            self.confidence_threshold = 0.85
            self.risk_level = 0.01



        return {
            "confidence_threshold":
                self.confidence_threshold,

            "risk_level":
                self.risk_level,

            "report":
                report
        }
