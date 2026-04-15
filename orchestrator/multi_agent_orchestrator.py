# orchestrator/multi_agent_orchestrator.py
import asyncio
import os
from typing import Dict, List, Any
from datetime import datetime

from anthropic import AsyncAnthropic          # Claude
from openai import AsyncOpenAI                # ChatGPT + Grok (xAI)
import google.generativeai as genai           # Gemini

from ..core.core_engine import BetaRootCoreEngine
from ..core.consistency_checker import ConsistencyChecker
from ..core.causal_graph import CausalGraphBuilder
from ..core.frequency_resonance import FrequencyResonance

class ExternalAgent:
    def __init__(self, name: str, client, model: str):
        self.name = name
        self.client = client
        self.model = model

class MultiAgentOrchestrator:
    """
    BetaRoot Ω → الدماغ المركزي الذي يتحكم في Claude, Grok, Gemini, ChatGPT
    """

    def __init__(self):
        self.core = BetaRootCoreEngine()                     # نواة BetaRoot
        self.consistency = ConsistencyChecker()
        self.causal = CausalGraphBuilder()
        self.resonance = FrequencyResonance()

        # إعداد الوكلاء الخارجيين (استخدم مفاتيح API من .env)
        self.agents = {
            "claude": ExternalAgent("Claude", AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY")), "claude-3-7-sonnet-20250219"),
            "grok": ExternalAgent("Grok", AsyncOpenAI(api_key=os.getenv("XAI_API_KEY"), base_url="https://api.x.ai/v1"), "grok-3"),
            "gemini": ExternalAgent("Gemini", None, "gemini-2.0-flash"),   # genai.configure(api_key=...)
            "chatgpt": ExternalAgent("ChatGPT", AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY")), "gpt-4o"),
        }

    async def query_external_agent(self, agent_name: str, prompt: str) -> Dict:
        agent = self.agents[agent_name]
        try:
            if agent_name == "claude":
                resp = await agent.client.messages.create(model=agent.model, max_tokens=4096, messages=[{"role": "user", "content": prompt}])
                return {"agent": agent_name, "response": resp.content[0].text, "success": True}
            elif agent_name in ["grok", "chatgpt"]:
                resp = await agent.client.chat.completions.create(model=agent.model, messages=[{"role": "user", "content": prompt}], max_tokens=4096)
                return {"agent": agent_name, "response": resp.choices[0].message.content, "success": True}
            # Gemini مشابه...
            else:
                return {"agent": agent_name, "response": "Not implemented yet", "success": False}
        except Exception as e:
            return {"agent": agent_name, "response": str(e), "success": False}

    async def orchestrate(self, user_query: str) -> Dict:
        """الدورة الكاملة: توزيع → جمع → تحقق → دمج → تصحيح ترددي"""
        print(f"🚀 BetaRoot Orchestrator يعالج: {user_query}")

        # 1. توزيع المهمة على 4 وكلاء
        tasks = [self.query_external_agent(name, user_query) for name in self.agents.keys()]
        responses = await asyncio.gather(*tasks)

        # 2. جمع الإجابات
        raw_answers = {r["agent"]: r["response"] for r in responses if r["success"]}

        # 3. التحقق من الاتساق بـ BetaRoot Core
        validated = []
        for agent, answer in raw_answers.items():
            check = self.consistency.verify(answer, context=user_query)
            if check["is_consistent"]:
                validated.append((agent, answer))

        # 4. دمج في Causal Graph
        for agent, answer in validated:
            self.causal.add_relation(f"Query: {user_query}", "answered_by", f"{agent}: {answer[:100]}...")

        # 5. تصحيح ترددي (Schumann)
        signal = await self.core.signal_layer.monitor_real_time()
        if signal["correction_needed"]:
            print("⚠️ ضغط ترددي خاطئ → تفعيل Anti-Virus Pattern")
            # تطبيق نمط تصحيح

        # 6. النتيجة النهائية من BetaRoot
        final = await self.core.process_fused(validated)   # دالة ستُضاف لاحقاً

        return {
            "query": user_query,
            "raw_responses": raw_answers,
            "validated_count": len(validated),
            "final_answer": final["answer"],
            "explanation": final["explanation"],
            "causal_graph_summary": self.causal.get_stats(),
            "schumann_pressure": signal["wrong_pressure"]["wrong_pressure"],
            "timestamp": datetime.now().isoformat()
        }

from .validation_layer import ValidationLayer
from .fusion_engine import FusionEngine

class MultiAgentOrchestrator:
    def __init__(self):
        self.validation = ValidationLayer()
        self.fusion = FusionEngine()
        # ... (الـ agents الخارجيين كما في الرد السابق)

    async def orchestrate(self, user_query: str) -> Dict:
        # 1. توزيع على الوكلاء الخارجيين
        tasks = [self.query_external_agent(name, user_query) for name in self.agents]
        raw_responses = {r["agent"]: r["response"] for r in await asyncio.gather(*tasks) if r["success"]}

        # 2. التحقق + الدمج
        validation_result = await self.validation.validate_and_fuse(raw_responses, user_query)

        # 3. الدمج النهائي + Self-Evolution
        final_result = await self.fusion.fuse_and_evolve(validation_result, user_query)

        return final_result

# داخل orchestrate()
final_result = await self.fusion.fuse_and_evolve(validation_result, user_query)

# تشغيل Self-Evolution بعد كل دورة كبيرة
if len(validation_result.get("validated_count", 0)) > 2:
    await self.core.evolve({"correction_needed": validation_result.get("correction_needed", False)})

from ..frequency.multi_agent_consciousness import MultiAgentFrequencyConsciousness

class MultiAgentOrchestrator:
    def __init__(self):
        self.freq_consciousness = MultiAgentFrequencyConsciousness(num_agents=12)

    async def orchestrate(self, user_query: str):
        # ... باقي الكود ...
        consciousness_report = await self.freq_consciousness.run_global_cycle(user_query)
        
        print(f"🌌 Collective Consciousness: {consciousness_report['global_consciousness']:.3f} | Decision: {consciousness_report['decision']}")

from ..bit_layer import BitLayer
from ..frequency.visualization import FrequencyVisualizer

class MultiAgentOrchestrator:
    def __init__(self):
        self.bit_layer = BitLayer()
        self.visualizer = FrequencyVisualizer()

    async def orchestrate(self, user_query: str):
        # معالجة باستخدام Bits
        bits = await self.bit_layer.process_signal_to_bits()
        bit_state = self.bit_layer.compute_collective_bit_state()

        # عرض الـ Visualization (في الـ Dashboard)
        # self.visualizer.plot_phase_space(bits)

        # ربط مع Sandbox قبل أي قرار
        if bit_state["emergence_potential"] > 0.65:
            # اقتراح تطور آمن
            proposal_result = await self.core.sandbox.propose_change(
                module="bit_layer",
                parameter="resonance_threshold",
                new_value=0.78,
                reason=f"High emergence potential detected: {bit_state['emergence_potential']:.3f}"
            )

        return {
            "bit_state": bit_state,
            "bits_count": len(bits),
            "emergence_potential": bit_state["emergence_potential"],
            "recommendation": "resonate" if bit_state["emergence_potential"] > 0.65 else "explore"
        }

from ..bit_layer import BitLayer
from ..orchestrator.sandbox_engine import SandboxEngine
from ..frequency.visualization import PlantFrequencyVisualizer

class MultiAgentOrchestrator:
    def __init__(self):
        self.bit_layer = BitLayer()
        self.sandbox = SandboxEngine(GovernanceEngine())
        self.visualizer = PlantFrequencyVisualizer()

    async def orchestrate(self, user_query: str):
        # 1. استيعاب إشارات نباتية → Bits
        plants = ["oak", "banyan", "sequoia", "pine"]
        for plant in plants:
            # محاكاة إشارة نباتية
            signal = np.sin(2 * np.pi * 7.8 * np.linspace(0, 5, 800)) + np.random.normal(0, 0.07, 800)
            await self.bit_layer.ingest_plant_signal(plant, signal)

        # 2. حساب حالة الـ Bits
        bit_state = self.bit_layer.compute_collective_bit_state()

        # 3. Sandbox + Self-Evolution
        if bit_state["emergence_potential"] > 0.68:
            top_bit = max(self.bit_layer.bits, key=lambda b: b.consciousness_contribution)
            result = await self.sandbox.propose_genetic_change(
                bit=top_bit,
                new_value=min(0.98, top_bit.consciousness_contribution + 0.05),
                reason=f"High emergence from {top_bit.plant_source} plant"
            )
            print(f"Sandbox Result: {result['status']} | Plant: {result.get('plant', '')}")

        # 4. Visualization
        self.visualizer.plot_genetic_bits(self.bit_layer.bits, self.bit_layer.plant_db)
        self.visualizer.plot_plant_resonance_radar(self.bit_layer.plant_db)

        return {
            "query": user_query,
            "bit_state": bit_state,
            "nature_consciousness": self.bit_layer.get_nature_consciousness(),
            "recommendation": "resonate_with_nature" if bit_state["emergence_potential"] > 0.7 else "explore"
        }
