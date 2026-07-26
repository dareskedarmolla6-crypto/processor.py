from brain.memory_manager import MemoryManager
from brain.reward_engine import RewardEngine
from brain.closed_trade_handler import ClosedTradeHandler
from brain.self_optimizer import SelfOptimizer
from brain.adaptive_brain import AdaptiveBrain
from brain.execution_engine import ExecutionEngine
from brain.position_manager import PositionManager


class AutonomousControllerV2:
    """
    FSE Autonomous Brain Controller V2

    Flow:

    Signal
      ↓
    AdaptiveBrain
      ↓
    Execution
      ↓
    PositionManager
      ↓
    Learning
      ↓
    Optimization
      ↓
    State Recovery
    """

    def __init__(self, db="autonomous_controller_v2.db"):

        self.memory = MemoryManager(db)

        self.reward = RewardEngine(
            self.memory
        )

        self.handler = ClosedTradeHandler(
            self.reward
        )

        self.optimizer = SelfOptimizer(
            self.memory
        )

        self.brain = AdaptiveBrain(
            self.memory,
            min_confidence=0.70
        )

        self.execution = ExecutionEngine()

        self.position_manager = PositionManager(
            execution=self.execution
        )


    # ---------------------------------
    # BRAIN DECISION
    # ---------------------------------

    def decide(self, signal):

        state = self.optimizer.optimize()

        decision = self.brain.evaluate(
            signal
        )

        return {
            "brain_state": state,
            "decision": decision
        }



    # ---------------------------------
    # EXECUTE TRADE
    # ---------------------------------

    def execute(self, symbol, signal, price):

        result = self.position_manager.manage(
            symbol,
            signal,
            price
        )

        return result



    # ---------------------------------
    # LEARN FROM CLOSED POSITION
    # ---------------------------------

    def learn(self, position):

        return self.handler.process_closed_position(
            position
        )



    # ---------------------------------
    # OPTIMIZE AFTER LEARNING
    # ---------------------------------

    def optimize(self):

        return self.optimizer.optimize()



    # ---------------------------------
    # RECOVERY STATE
    # ---------------------------------

    def recover_state(self):

        return {
            "memory": self.memory.history,
            "optimizer": self.optimizer.optimize()
        }



    def close(self):

        self.memory.close()
