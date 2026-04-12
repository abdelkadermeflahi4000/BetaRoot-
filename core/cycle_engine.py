# core/cycle_engine.py

from typing import Callable, Dict, List, Any, Optional
import time


# ========================
# 🧬 State Definition
# ========================

class CycleState:
    def __init__(
        self,
        name: str,
        action: Callable[[Dict], Dict],
        duration: float = 0.0,
        metadata: Optional[Dict] = None
    ):
        self.name = name
        self.action = action
        self.duration = duration
        self.metadata = metadata or {}

    def execute(self, system_state: Dict) -> Dict:
        return self.action(system_state)


# ========================
# 🔁 Transition Controller
# ========================

class TransitionController:
    def __init__(self, states: List[CycleState]):
        self.states = {s.name: s for s in states}
        self.order = [s.name for s in states]

    def next(self, current_name: str) -> str:
        idx = self.order.index(current_name)
        return self.order[(idx + 1) % len(self.order)]

    def get(self, name: str) -> CycleState:
        return self.states[name]


# ========================
# 🧠 Feedback System
# ========================

class FeedbackSystem:
    def evaluate(self, prev_state: Dict, new_state: Dict) -> Dict:
        return {
            "delta": {
                k: new_state.get(k, 0) - prev_state.get(k, 0)
                for k in new_state
            }
        }


# ========================
# 🧠 Memory Interface (plug-in)
# ========================

class CycleMemory:
    def __init__(self):
        self.history = []

    def store(self, entry: Dict):
        self.history.append(entry)

    def get_last(self):
        return self.history[-1] if self.history else None


# ========================
# 🤖 Agent Interface (optional)
# ========================

class CycleAgent:
    def decide(self, system_state: Dict, feedback: Dict) -> Optional[str]:
        """
        Return next state name or None for default transition
        """
        return None


# ========================
# 🌍 World Adapter (optional)
# ========================

class WorldAdapter:
    def observe(self) -> Dict:
        return {}

    def apply(self, state: Dict):
        pass


# ========================
# 🚀 Core Cycle Engine
# ========================

class CycleEngine:
    def __init__(
        self,
        states: List[CycleState],
        agent: Optional[CycleAgent] = None,
        memory: Optional[CycleMemory] = None,
        feedback_system: Optional[FeedbackSystem] = None,
        world: Optional[WorldAdapter] = None,
        sleep: float = 0.0
    ):
        self.controller = TransitionController(states)
        self.agent = agent or CycleAgent()
        self.memory = memory or CycleMemory()
        self.feedback = feedback_system or FeedbackSystem()
        self.world = world or WorldAdapter()

        self.current_state_name = states[0].name
        self.sleep = sleep

    def step(self, system_state: Dict) -> Dict:
        state_obj = self.controller.get(self.current_state_name)

        prev_state = dict(system_state)

        # 🔧 Execute state logic
        new_state = state_obj.execute(system_state)

        # 🧠 Feedback
        feedback = self.feedback.evaluate(prev_state, new_state)

        # 🤖 Agent decision
        decision = self.agent.decide(new_state, feedback)

        if decision and decision in self.controller.states:
            next_state = decision
        else:
            next_state = self.controller.next(self.current_state_name)

        # 🧠 Memory store
        self.memory.store({
            "state": self.current_state_name,
            "next": next_state,
            "data": new_state,
            "feedback": feedback
        })

        # 🌍 Apply to world
        self.world.apply(new_state)

        # 🔁 Transition
        self.current_state_name = next_state

        if state_obj.duration > 0 or self.sleep > 0:
            time.sleep(max(state_obj.duration, self.sleep))

        return new_state

    def run(self, initial_state: Dict, steps: int = 10) -> Dict:
        state = initial_state
        for _ in range(steps):
            observed = self.world.observe()
            state.update(observed)

            state = self.step(state)

        return state


# ========================
# 🧪 Example Use (can remove in production)
# ========================

if __name__ == "__main__":

    def fill(s):
        s["water"] = s.get("water", 0) + 10
        return s

    def wash(s):
        s["dirt"] = s.get("dirt", 1.0) * 0.5
        return s

    def spin(s):
        s["water"] = s.get("water", 0) * 0.2
        return s

    states = [
        CycleState("Fill", fill),
        CycleState("Wash", wash),
        CycleState("Spin", spin),
    ]

    engine = CycleEngine(states)

    final = engine.run({"water": 0, "dirt": 1.0}, steps=6)

    print(final)
