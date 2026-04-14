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

from core.conflict_engine import ConflictEngine
from core.emergence import EmergenceTracker

class BetaRootEngine:

    def __init__(self, agents):
        ...
        self.conflict = ConflictEngine()
        self.emergence = EmergenceTracker()

    def cycle(self):
        signal = self.signal_engine.generate()

        decisions = self.orchestrator.run_agents(self.state, signal)

        # ⚔️ حل الصراع
        winner = self.conflict.resolve(decisions)

        if winner:
            action = winner["action"]

            print("[ACTION]", action)

            self.state.update("last_action", action)

            # 🌊 تتبع الانبثاق
            self.emergence.track(winner)

            pattern = self.emergence.detect_pattern()

            if pattern:
                print("[EMERGENCE]", pattern)

        # 🔬 التطور
        self.evolve_system()

from core.memory.emergent_memory import EmergentMemory
from core.memory.concept_builder import ConceptBuilder
from core.memory.symbol_encoder import SymbolEncoder
from core.language.internal_language import InternalLanguage
from core.language.grammar_engine import GrammarEngine

class BetaRootEngine:

    def __init__(self, agents):
        ...
        self.memory = EmergentMemory()
        self.concept_builder = ConceptBuilder()
        self.encoder = SymbolEncoder()
        self.language = InternalLanguage()
        self.grammar = GrammarEngine()

    def cycle(self):
        ...
        if winner:
            action = winner["action"]

            # 🧠 تخزين
            self.memory.store(action)

            # 🧬 استخراج الأنماط
            patterns = self.memory.extract_patterns()

            # 🧠 بناء المفاهيم
            concepts = self.concept_builder.build(patterns)

            # 🔤 توليد رموز
            for name in concepts:
                symbol = self.encoder.encode(name)
                self.language.register(name, symbol)

            # 🗣️ لغة داخلية
            expression = self.language.express()
            print("[LANG]", expression)

            # 📜 قواعد
            symbols = list(self.language.dictionary.keys())
            rule = self.grammar.generate(symbols)

            if rule:
                print("[GRAMMAR]", rule)
