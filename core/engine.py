# core/engine.py

import time
from core.state import SystemState
from core.signals import SignalEngine
from core.orchestrator import Orchestrator
from core.evolution import EvolutionEngine

class BetaRootEngine:

    def __init__(self, agents):
        self.state = SystemState()
        self.signal_engine = SignalEngine()
        self.orchestrator = Orchestrator(agents)
        self.evolution = EvolutionEngine()

    def cycle(self):
        # 1. الإشارة (التردد)
        signal = self.signal_engine.generate()

        # 2. تشغيل الوكلاء
        decisions = self.orchestrator.run_agents(self.state, signal)

        # 3. حل القرارات
        actions = self.orchestrator.resolve(decisions)

        # 4. تنفيذ
        for action in actions:
            print("[ACTION]", action)
            self.state.update("last_action", action)

        # 5. التطور
        self.evolution.evolve(self.state)

    def run(self):
        print("🚀 BetaRoot Engine Started")

        while True:
            self.cycle()
            time.sleep(0.1)
