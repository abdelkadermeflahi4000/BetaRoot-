# betaroot/core/inference/multi_expert.py
import asyncio
from typing import Dict, List, Callable
from ..knowledge.knowledge_base import KnowledgeBase
from ..knowledge.fact_base import FactBase
from .orchestrator import InferenceOrchestrator, InferenceResult

class MultiExpertOrchestrator:
    def __init__(self):
        self.experts: Dict[str, InferenceOrchestrator] = {}
        self.routing_rules: Dict[str, Callable[[str], bool]] = {}
        
    def register_expert(self, domain: str, orchestrator: InferenceOrchestrator, 
                        routing_fn: Callable[[str], bool]):
        self.experts[domain] = orchestrator
        self.routing_rules[domain] = routing_fn
        
    async def infer_parallel(self, query: str, evidence: dict) -> Dict[str, InferenceResult]:
        """يشغّل كل الخبراء المناسبين بالتوازي ويجمع النتائج"""
        tasks = []
        for domain, orchestrator in self.experts.items():
            if self.routing_rules[domain](query):
                tasks.append(self._run_expert(domain, orchestrator, query, evidence))
                
        results = await asyncio.gather(*tasks)
        merged = {}
        for res in results:
            merged.update(res)
        return merged
        
    async def _run_expert(self, domain, orchestrator, query, evidence):
        try:
            return await asyncio.to_thread(
                orchestrator.infer, query, evidence=evidence
            )
        except Exception as e:
            return {query: InferenceResult(query, "ERROR", 0.0, f"{domain}_error", [str(e)])}
