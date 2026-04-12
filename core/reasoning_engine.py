# core/reasoning_engine.py

class ReasoningEngine:
    def __init__(self, memory_store, mode_engine):
        self.memory = memory_store
        self.mode_engine = mode_engine

    def reason(self, query: dict):
        mode = self.mode_engine.auto_select_mode(query)

        if mode == "theta":
            return self.deep_memory(query)
        elif mode == "alpha":
            return self.creative_reasoning(query)
        elif mode == "beta":
            return self.strict_logic(query)
        elif mode == "gamma":
            return self.integrative_reasoning(query)

    def deep_memory(self, query):
        results = self.memory.search(query["text"])
        return {
            "mode": "theta",
            "results": results
        }

    def creative_reasoning(self, query):
        return {
            "mode": "alpha",
            "idea": f"Possible hypothesis about '{query['text']}'"
        }

    def strict_logic(self, query):
        facts = self.memory.search(query["text"])
        return {
            "mode": "beta",
            "logic_chain": facts
        }

    def integrative_reasoning(self, query):
        facts = self.memory.search(query["text"])
        return {
            "mode": "gamma",
            "synthesis": facts
        }
