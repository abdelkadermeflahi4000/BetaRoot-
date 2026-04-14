# core/core_engine.py
import asyncio
from datetime import datetime

from .real_signal_layer import RealSignalLayer
from .frequency_guardian import FrequencyGuardian
from .memory_system import BetaRootMemorySystem, MemoryType, Priority
from .consolidation_engine import ConsolidationEngine
from .governance import GovernanceEngine, Action
from .encryption_rotator import EncryptionRotator
from .agents.multi_agent import MultiAgentSystem

class BetaRootCoreEngine:
    def __init__(self):
        self.signal_layer = RealSignalLayer()          # الطبقة الجديدة
        self.guardian = FrequencyGuardian()
        self.memory = BetaRootMemorySystem()
        self.consolidator = ConsolidationEngine(self.memory)
        self.governance = GovernanceEngine(mode="strict")
        self.rotator = EncryptionRotator()
        self.agents = MultiAgentSystem()

        self.running = False
        self.cycle_count = 0

    async def observe(self):
        """المرحلة 1: مراقبة الإشارات الحقيقية"""
        signal_data = await self.signal_layer.monitor_real_time()
        return {
            "signal": signal_data,
            "frequency_status": signal_data["wrong_pressure"],
            "timestamp": datetime.now().isoformat()
        }

    async def evolve(self, cycle_data: dict):
        """Self-Evolution الحقيقي"""
        # 1. اكتشاف أنماط جديدة
        if cycle_data["signal"].get("correction_needed"):
            self.resonance.k_tech = min(0.4, self.resonance.k_tech + 0.015)  # تعلم ذاتي

        # 2. دمج الذاكرة
        if self.cycle_count % 5 == 0:
            self.consolidator.consolidate()

        # 3. تسجيل التطور
        self.memory.store({
            "cycle": self.cycle_count,
            "evolution_type": "frequency_calibration" if cycle_data["signal"].get("correction_needed") else "stability",
            "pressure": cycle_data["signal"]["wrong_pressure"]["wrong_pressure"]
        }, MemoryType.EPISODIC, Priority.HIGH, source="SelfEvolution")

        print(f"🔄 Self-Evolution completed | Cycle {self.cycle_count} | Pressure: {cycle_data['signal']['wrong_pressure']['wrong_pressure']}")

    async def run_cycle(self):
        self.cycle_count += 1
        print(f"\n🔥 Core Cycle #{self.cycle_count} @ {datetime.now().strftime('%H:%M:%S')}")

        obs = await self.observe()

        action = Action.ACTIVATE_CORRECTION if obs["signal"]["correction_needed"] else Action.MAINTAIN_STABILITY
        if not self.governance.check(action):
            return

        self.memory.store(obs, MemoryType.EPISODIC, Priority.HIGH, "RealSignalLayer")

        await self.evolve(obs)

        print(f"✅ Cycle done | Signal Quality: {obs['signal']['signal_quality']}")

    async def start(self):
        self.running = True
        print("🌌 BetaRoot Ω Core Engine يعمل الآن مع إشارات Schumann الحية...")

        # تشغيل تدوير التشفير
        asyncio.create_task(self.rotator.start_rotation())

        while self.running:
            await self.run_cycle()
            await asyncio.sleep(25)   # دورة كل 25 ثانية

    def stop(self):
        self.running = False
        print("⏹️ Core Engine تم إيقافه.")

class BetaRootCoreEngine:
    def __init__(self):
        self.signal_layer = RealSignalLayer()          # ← التكامل الجديد
        # ... باقي الـ init السابق ...

    async def observe(self):
        """الآن يعتمد على Schumann الحي"""
        signal_data = await self.signal_layer.monitor_real_time()
        return {
            "signal": signal_data,
            "frequency_status": signal_data["wrong_pressure"],
            "timestamp": datetime.now().isoformat()
        }

    async def run_cycle(self):
        self.cycle_count += 1
        print(f"\n🔥 Cycle #{self.cycle_count} | Schumann Source: {self.signal_layer.last_data.get('source', 'N/A')}")

        obs = await self.observe()

        action = Action.ACTIVATE_CORRECTION if obs["signal"]["correction_needed"] else Action.MAINTAIN_STABILITY
        if not self.governance.check(action):
            return

        self.memory.store(obs, MemoryType.EPISODIC, Priority.HIGH, source="RealSignalLayer")

        await self.evolve(obs)          # Self-Evolution يتعلم من الترددات

        print(f"✅ Schumann integrated | Freq: {obs['signal']['dominant_frequency']} Hz | Quality: {obs['signal']['signal_quality']}")

# داخل __init__
self.sandbox = SandboxEngine(self.governance)

# داخل دالة evolve()
async def evolve(self, cycle_data: dict):
    self.cycle_count += 1
    
    if cycle_data.get("correction_needed", False):
        # اقتراح تعديل ذاتي آمن
        proposal_result = await self.sandbox.propose_change(
            module="resonance",
            parameter="k_conscious",
            new_value=max(0.05, self.resonance.k_conscious - 0.025),
            reason="Schumann wrong pressure detected → reducing conscious contamination",
            proposed_by="frequency_guardian"
        )
        
        if proposal_result["status"] == "approved":
            print(f"✅ Self-Evolution successful: {proposal_result['proposal_id']}")
        else:
            print(f"⛔ Self-Evolution rejected by Sandbox: {proposal_result['reason']}")

    # تقرير Sandbox دوري
    if self.cycle_count % 10 == 0:
        report = self.sandbox.get_sandbox_report()
        print(f"📊 Sandbox Report → Approved: {report['approved_count']} | Rejected: {report['rejected_count']}")
