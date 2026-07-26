import time


class LiveAutonomousLoop:
    """
    FSE Live Autonomous Loop Engine

    Flow:

    Market
      ↓
    Brain
      ↓
    Allocation
      ↓
    Risk
      ↓
    Execution
      ↓
    Reward
      ↓
    Learning
    """

    def __init__(
        self,
        brain,
        allocator,
        governor,
        position_manager,
        reward_engine=None
    ):

        self.brain = brain
        self.allocator = allocator
        self.governor = governor
        self.position_manager = position_manager
        self.reward_engine = reward_engine

        self.running = False



    # -------------------------
    # Single Cycle
    # -------------------------
    def run_cycle(
        self,
        market,
        balance=1000
    ):

        print("\n========== LIVE CYCLE ==========")


        # 1. Brain Decision

        brain_result = self.brain.process(
            market
        )


        print("\nBRAIN:")
        print(brain_result)



        # 2. Filter Trades

        opportunities = [

            x for x in brain_result

            if x["decision"] == "TRADE"

        ]



        # 3. Capital Allocation

        allocations = self.allocator.allocate(

            balance,

            [

                {
                    "symbol": x["symbol"],
                    "confidence": x["confidence"]
                }

                for x in opportunities

            ]

        )


        print("\nALLOCATIONS:")
        print(allocations)



        # 4. Risk Governor

        status = self.governor.approve_trade()


        print("\nRISK:")
        print(status)



        if status[0] is False:

            return {

                "status": "BLOCKED",

                "reason": status[1]

            }



        # 5. Execution

        trades = []


        for symbol, amount in allocations.items():

            signal = next(

                x for x in opportunities

                if x["symbol"] == symbol

            )


            trade = self.position_manager.manage(

                symbol,

                {
                    "signal": signal["signal"]
                },

                price=signal.get(
                    "price",
                    0
                ),

                balance=balance,

                stop_loss_price=None

            )


            trades.append(

                {
                    "symbol": symbol,
                    "trade": trade
                }

            )



        print("\nTRADES:")
        print(trades)



        return {

            "brain": brain_result,

            "allocations": allocations,

            "trades": trades

        }



    # -------------------------
    # Continuous Loop
    # -------------------------
    def start(
        self,
        market_provider,
        interval=10
    ):

        self.running = True


        while self.running:


            market = market_provider()


            self.run_cycle(
                market
            )


            time.sleep(
                interval
            )



    # -------------------------
    # Stop Loop
    # -------------------------
    def stop(self):

        self.running = False
