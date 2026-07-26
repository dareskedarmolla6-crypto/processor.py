from brain.feedback_loop import FeedbackLoop


class LiveLearningLoop:
    """
    FSE Live Autonomous Learning Loop

    Live Trade Cycle:

    Market
       ↓
    Brain Decision
       ↓
    Execution
       ↓
    Trade Result
       ↓
    Feedback Loop
       ↓
    Memory Update
       ↓
    Optimization
       ↓
    Brain Improvement
    """


    def __init__(
        self,
        brain,
        execution_engine,
        feedback_loop
    ):

        self.brain = brain
        self.execution = execution_engine
        self.feedback = feedback_loop



    # -------------------------
    # Execute Live Cycle
    # -------------------------
    def run(
        self,
        signals
    ):

        result = {
            "decisions": [],
            "trades": [],
            "feedback": [],
            "learning": None
        }


        # Brain decision
        decisions = self.brain.process(
            signals
        )

        result["decisions"] = decisions



        # Execute trades
        for decision in decisions:

            if decision["decision"] != "TRADE":
                continue


            trade = self.execution.execute(
                decision
            )


            result["trades"].append(
                {
                    "symbol": decision["symbol"],
                    "trade": trade
                }
            )



        return result



    # -------------------------
    # Receive Closed Trades
    # -------------------------
    def update_feedback(
        self,
        closed_trades
    ):

        feedback = self.feedback.process_batch(
            closed_trades
        )


        learning = self.feedback.learn()


        return {
            "feedback": feedback,
            "learning": learning
        }
