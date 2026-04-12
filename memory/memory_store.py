# memory/memory_store.py

import uuid

class MemoryStore:
    def __init__(self):
        self.storage = {}

    def add_fact(self, content, fact_type="fact", mode="theta", confidence=1.0):
        fact_id = str(uuid.uuid4())

        self.storage[fact_id] = {
            "id": fact_id,
            "content": content,
            "type": fact_type,
            "mode": mode,
            "confidence": confidence,
            "causal_links": []
        }

        return fact_id

    def link_facts(self, source_id, target_id):
        if source_id in self.storage:
            self.storage[source_id]["causal_links"].append(target_id)

    def get_by_mode(self, mode):
        return [
            fact for fact in self.storage.values()
            if fact["mode"] == mode
        ]

    def search(self, keyword):
        return [
            fact for fact in self.storage.values()
            if keyword.lower() in fact["content"].lower()
        ]
