# betaroot/core/explanation/generator.py
from typing import List
from ..knowledge.fact_base import FactBase, TruthValue
from ..knowledge.knowledge_base import KnowledgeBase, Rule

class ExplanationGenerator:
    @staticmethod
    def generate_trace(facts: FactBase, kb: KnowledgeBase, hypothesis: str) -> str:
        lines = [f"📊 تقرير الاستدلال للفرضية: {hypothesis}"]
        fact = facts.get(hypothesis)
        if not fact:
            return f"❌ لا يوجد استنتاج لـ {hypothesis} في قاعدة الحقائق الحالية."
            
        lines.append(f"✅ النتيجة: {fact.value} (يقين: {fact.confidence:.2%})")
        lines.append(f"📝 المصدر: {fact.source}")
        if fact.justification:
            rule = kb.get_rule(fact.justification)
            if rule:
                lines.append(f"🔗 القاعدة المطبقة: {rule}")
                lines.append(f"   المقدمات: {', '.join(rule.antecedents)}")
                
        lines.append("\n📜 سجل الأدلة المؤثرة:")
        for entry in facts.get_history(limit=10):
            if entry.action in ("add", "update", "revise"):
                lines.append(f"  • {entry.timestamp.strftime('%H:%M:%S')} | {entry.variable} ← {entry.action}")
                
        return "\n".join(lines)
