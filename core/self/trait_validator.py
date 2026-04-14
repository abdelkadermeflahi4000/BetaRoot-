# core/self/trait_validator.py

class TraitValidator:

    def validate(self, trait, state):
        activity = len(state.history)

        # مثال بسيط
        if activity > 5:
            return True

        return False
