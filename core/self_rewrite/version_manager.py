# core/self_rewrite/version_manager.py

class VersionManager:

    def __init__(self):
        self.versions = []

    def save(self, code):
        self.versions.append(code)

    def rollback(self):
        if self.versions:
            return self.versions[-1]
