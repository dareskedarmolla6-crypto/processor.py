class PortfolioFeedback:
    """
    FSE Portfolio Feedback Intelligence V7.7

    Converts portfolio behavior into brain feedback.

    STRONG  -> increase confidence
    WEAK    -> reduce confidence
    """

    def __init__(self, portfolio_memory):

        self.memory = portfolio_memory
        self.history = []


    def analyze(self):

        feedback = {}

        # Get latest portfolio state
        portfolio = self.memory.get()


        for symbol, data in portfolio.items():

            action = data.get("action", "HOLD")
            allocation = data.get("allocation", 0)


            if action == "INCREASE":

                feedback[symbol] = {
                    "adjustment": 0.05,
                    "decision": "BOOST",
                    "reason": "STRONG_PORTFOLIO",
                    "allocation": allocation
                }


            elif action == "REDUCE":

                feedback[symbol] = {
                    "adjustment": -0.10,
                    "decision": "PENALIZE",
                    "reason": "WEAK_PORTFOLIO",
                    "allocation": allocation
                }


            else:

                feedback[symbol] = {
                    "adjustment": 0,
                    "decision": "HOLD",
                    "reason": "NO_CHANGE",
                    "allocation": allocation
                }


        self.history.append(feedback)

        return feedback


    def get_history(self):

        return self.history
