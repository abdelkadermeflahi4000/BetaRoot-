# core/architecture/architecture_generator.py

import random

class ArchitectureGenerator:

    def generate(self, base):
        new_arch = base.copy()

        # إضافة وكيل جديد
        if random.random() > 0.5:
            new_arch["agents"].append("adaptive_" + str(random.randint(1, 100)))

        # تغيير loop
        if random.random() > 0.5:
            new_arch["loops"].append("reflective_loop")

        return new_arch
