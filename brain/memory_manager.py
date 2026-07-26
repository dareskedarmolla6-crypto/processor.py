from brain.performance_memory import PerformanceMemory
from brain.persistent_memory import PersistentMemory


class MemoryManager:
    """
    FSE Memory Manager

    Live Brain Memory
          +
    Persistent Storage
    """


    def __init__(
        self,
        db_path="fse_memory.db"
    ):

        self.live_memory = PerformanceMemory()

        self.storage = PersistentMemory(
            db_path
        )

        self._load_history()



    # -------------------------
    # Restore Memory
    # -------------------------
    def _load_history(self):

        history = self.storage.load_history()

        if not history:
            return


        for symbol, data in history.items():

            self.live_memory.history[symbol] = data



    # -------------------------
    # Record Result
    # -------------------------
    def record(
        self,
        symbol,
        pnl
    ):

        # Update live brain

        self.live_memory.record(
            symbol,
            pnl
        )


        # Save permanent

        self.storage.save_trade(
            symbol,
            pnl
        )



    # -------------------------
    # Symbol Score
    # -------------------------
    def score(
        self,
        symbol
    ):

        return self.live_memory.score(
            symbol
        )



    # -------------------------
    # Confidence Learning
    # -------------------------
    def adjust_confidence(
        self,
        symbol,
        confidence
    ):

        return self.live_memory.adjust_confidence(
            symbol,
            confidence
        )



    # -------------------------
    # History Access
    # -------------------------
    @property
    def history(self):

        return self.live_memory.history



    # -------------------------
    # Shutdown
    # -------------------------
    def close(self):

        self.storage.close()
