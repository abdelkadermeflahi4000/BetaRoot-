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
