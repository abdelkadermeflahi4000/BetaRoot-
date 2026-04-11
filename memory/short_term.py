class ShortTermMemory:
    def __init__(self, max_size=10):
        self.buffer = []
        self.max_size = max_size

    def add(self, item):
        self.buffer.append(item)

        if len(self.buffer) > self.max_size:
            self.buffer.pop(0)

    def get_all(self):
        return self.buffer
