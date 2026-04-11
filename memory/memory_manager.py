from .short_term import ShortTermMemory
from .working_memory import WorkingMemory
from .long_term import LongTermMemory
from .episodic_memory import EpisodicMemory


class MemoryManager:
    def __init__(self):
        self.stm = ShortTermMemory()
        self.wm = WorkingMemory()
        self.ltm = LongTermMemory()
        self.em = EpisodicMemory()

    # ----------------------------------
    # Store new knowledge
    # ----------------------------------
    def store_fact(self, fact):
        self.stm.add(fact)
        self.ltm.add(fact)

    # ----------------------------------
    # Store reasoning session
    # ----------------------------------
    def store_episode(self, episode):
        self.em.record(episode)

    # ----------------------------------
    # Working memory
    # ----------------------------------
    def set_context(self, key, value):
        self.wm.set(key, value)

    def get_context(self, key):
        return self.wm.get(key)

    # ----------------------------------
    # Retrieve all knowledge
    # ----------------------------------
    def retrieve_all(self):
        return {
            "short_term": self.stm.get_all(),
            "long_term": self.ltm.get_all(),
            "episodic": self.em.get_all()
        }
