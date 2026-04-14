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

# داخل engine.py

from core.self.identity_core import IdentityCore
from core.self.identity_mutator import IdentityMutator
from core.self.identity_evaluator import IdentityEvaluator
from core.self.identity_manager import IdentityManager

class BetaRootEngine:

    def __init__(self, agents):
        ...
        self.identity = IdentityCore()
        self.identity_manager = IdentityManager(
            self.identity,
            IdentityMutator(),
            IdentityEvaluator()
        )

    def identity_cycle(self):
        self.identity_manager.evolve_identity(self.state)

        profile = self.identity.describe()

        print("[IDENTITY STATE]", profile)

        # تأثير الهوية على النظام
        self.state.update("traits", profile["traits"])

# داخل engine.py

from core.self.trait_generator import TraitGenerator
from core.self.trait_validator import TraitValidator
from core.self.trait_memory import TraitMemory
from core.self.open_identity_manager import OpenIdentityManager

class BetaRootEngine:

    def __init__(self, agents):
        ...
        self.trait_memory = TraitMemory()

        self.open_identity = OpenIdentityManager(
            self.identity,
            TraitGenerator(),
            TraitValidator(),
            self.trait_memory
        )

    def identity_cycle(self):
        # التطور العادي
        self.identity_manager.evolve_identity(self.state)

        # 💥 التوسع المفتوح
        self.open_identity.evolve(self.state)

        traits = self.identity.describe()["traits"]

        print("[TRAITS]", traits)

        self.state.update("traits", traits)

# داخل engine.py

from core.concepts.concept_memory import ConceptMemory
from core.concepts.theory_builder import TheoryBuilder
from core.concepts.theory_evaluator import TheoryEvaluator
from core.concepts.theory_engine import TheoryEngine

class BetaRootEngine:

    def __init__(self, agents):
        ...
        self.concept_memory = ConceptMemory()

        self.theory_engine = TheoryEngine(
            self.concept_memory,
            TheoryBuilder(),
            TheoryEvaluator()
        )

    def conceptual_cycle(self):
        # 1. أخذ المفاهيم من الذاكرة
        concepts = self.memory.patterns  # من Emergent Memory

        # 2. بناء النظرية
        theory = self.theory_engine.evolve(concepts)

        if theory:
            print("[THEORY]", theory["rules"])

            # 3. التأثير على القرار
            self.state.update("theory", theory)

# داخل engine.py

from core.world.world_engine import WorldEngine

class BetaRootEngine:

    def __init__(self, agents):
        ...
        self.world = WorldEngine()

    def decision_cycle(self):
        possible_actions = ["EXPLORE", "ANALYZE", "REST"]

        action, score = self.world.decide(self.state, possible_actions)

        print(f"[WORLD DECISION] {action} (score={score})")

        self.execute(action)

# داخل engine.py

from core.self_rewrite.rewrite_engine import RewriteEngine

class BetaRootEngine:

    def __init__(self, agents):
        ...
        self.rewriter = RewriteEngine()

    def evolution_cycle(self):
        self.rewriter.evolve(self.state.data)

# داخل engine.py

from core.architecture.architecture_engine import ArchitectureEngine

class BetaRootEngine:

    def __init__(self, agents):
        ...
        self.arch_engine = ArchitectureEngine()

    def architecture_cycle(self):
        best_arch = self.arch_engine.evolve(self.state.data)

        print("[ACTIVE ARCHITECTURE]", best_arch)

# داخل engine.py

from core.deployment.self_update import SelfUpdater

class BetaRootEngine:

    def __init__(self, agents):
        ...
        self.updater = SelfUpdater(repo_path=".")

    def background_tasks(self):
        import threading
        threading.Thread(target=self.updater.auto_update_loop).start()
