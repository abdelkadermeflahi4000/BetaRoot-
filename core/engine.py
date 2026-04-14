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

from core.self.self_model import SelfModel
from core.self.introspection import Introspection
from core.self.reflection import Reflection
from core.self.meta_controller import MetaController

class BetaRootEngine:

    def __init__(self, agents):
        ...
        self.self_model = SelfModel()
        self.introspection = Introspection()
        self.reflection = Reflection()
        self.meta = MetaController()

    def self_cycle(self):
        # تحديث الذات
        self.self_model.update(self.state)

        # تحليل داخلي
        insight = self.introspection.analyze(self.state)

        # انعكاس
        reflection = self.reflection.reflect(self.self_model, insight)

        print("[SELF]", self.self_model.describe())
        print("[REFLECTION]", reflection)

        # قرار ذاتي
        bias = self.meta.decide(self.self_model)

        # حقن التحيز داخل النظام
        self.state.update("bias", bias)

    def cycle(self):
        signal = self.signal_engine.generate()

        decisions = self.orchestrator.run_agents(self.state, signal)

        winner = self.conflict.resolve(decisions)

        if winner:
            action = winner["action"]

            self.state.update("last_action", action)

        # 🧠 الوعي الذاتي
        self.self_cycle()

        # 🧬 الذاكرة واللغة
        ...
        
        # 🔬 التطور
        self.evolve_system()

from core.self.identity_stack import IdentityStack
from core.self.layers import SelfLayers
from core.self.recursive_engine import RecursiveSelf

class BetaRootEngine:

    def __init__(self, agents):
        ...
        self.identity_stack = IdentityStack()
        self.self_layers = SelfLayers()
        self.recursive_self = RecursiveSelf(
            self.identity_stack,
            self.self_layers
        )

    def self_recursive_cycle(self):
        result = self.recursive_self.run(self.state)

        print("[L1 Awareness]", result["L1"])
        print("[L2 Reflection]", result["L2"])
        print("[L3 Strategy]", result["L3"])
        print("[L4 Meta]", result["L4"])

        # 🔥 التأثير على النظام
        strategy = result["L3"].get("strategy")

        if strategy == "increase exploration":
            self.state.update("bias", {"explore": 1.2})

        elif strategy == "increase reasoning":
            self.state.update("bias", {"reason": 1.2})

# داخل evolve() في CoreEngine
proposal_result = await self.sandbox.propose_change(
    module="resonance",
    parameter="k_conscious",
    new_value=0.12,   # خفض التلوث الوعي
    reason="Schumann wrong pressure detected in last cycle",
    proposed_by="frequency_guardian"
)

if proposal_result["status"] == "approved":
    print(f"🛡️ Sandbox approved safe evolution → new k_conscious = {proposal_result['new_value']}")
else:
    print(f"🚫 Sandbox blocked risky change: {proposal_result['reason']}")
