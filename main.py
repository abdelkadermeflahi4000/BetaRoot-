# main.py

from core.mode_engine import ModeEngine
from memory.memory_store import MemoryStore
from core.reasoning_engine import ReasoningEngine
from agents.multi_agent import MultiAgentSystem

# Initialize
mode_engine = ModeEngine()
memory = MemoryStore()

# Add knowledge
f1 = memory.add_fact("All humans are mortal", "axiom", "theta")
f2 = memory.add_fact("Socrates is a human", "fact", "beta")

memory.link_facts(f2, f1)

# Reasoning
engine = ReasoningEngine(memory, mode_engine)

multi_agent = MultiAgentSystem(engine)

query = {
    "text": "Socrates",
    "requires_proof": True,
    "complexity": "medium"
}

result = multi_agent.process(query)

print(result)
