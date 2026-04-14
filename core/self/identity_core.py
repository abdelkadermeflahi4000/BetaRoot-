# core/self/identity_core.py

class IdentityCore:

    def __init__(self):
        self.profile = {
            "type": "balanced",
            "traits": {
                "exploration": 1.0,
                "reasoning": 1.0,
                "stability": 1.0
            }
        }

    def update_trait(self, key, value):
        self.profile["traits"][key] = value

    def describe(self):
        return self.profile
