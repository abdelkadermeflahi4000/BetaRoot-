import json


class LongTermMemory:
    def __init__(self, filepath="memory.json"):
        self.filepath = filepath
        self.data = self._load()

    def _load(self):
        try:
            with open(self.filepath, "r") as f:
                return json.load(f)
        except:
            return []

    def save(self):
        with open(self.filepath, "w") as f:
            json.dump(self.data, f, indent=2)

    def add(self, item):
        self.data.append(item)
        self.save()

    def get_all(self):
        return self.data
