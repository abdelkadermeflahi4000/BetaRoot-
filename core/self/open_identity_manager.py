# core/self/open_identity_manager.py

class OpenIdentityManager:

    def __init__(self, identity, generator, validator, memory):
        self.identity = identity
        self.generator = generator
        self.validator = validator
        self.memory = memory

    def evolve(self, state):
        new_trait = self.generator.generate()

        print("[NEW TRAIT]", new_trait)

        if self.validator.validate(new_trait, state):
            self.memory.add(new_trait)

            # دمجها في الهوية
            self.identity.profile["traits"][new_trait["name"]] = new_trait["value"]

            print("[IDENTITY EXPANDED]", new_trait["name"])
        else:
            print("[TRAIT REJECTED]")
