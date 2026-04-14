# core/signals.py

import time
import math

class SignalEngine:

    def generate(self):
        t = time.time()

        return {
            "time": t,
            "wave": math.sin(t),
            "phase": t % (2 * math.pi)
        }
