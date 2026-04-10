# betaroot/core/analysis/diagnostic_analyzer.py
from typing import Dict, List, Optional
from ..knowledge.knowledge_base import KnowledgeBase
from ..knowledge.fact_base import FactBase, TruthValue
from ..inference.orchestrator import InferenceOrchestrator, InferenceStrategy
from ..inference.backward_chainer import BackwardChainer, ProofStatus
import copy

class DiagnosticAnalyzer:
    """
    وحدة التحليل واستكشاف الأخطاء في النظام الخبير
    تقدم: تتبع الجذور السببية، كشف التناقضات، محاكاة ماذا لو، وتوصيات تصحيحية
    """
    def __init__(self, kb: KnowledgeBase, fb: FactBase, orchestrator: InferenceOrchestrator):
        self.kb = kb
        self.fb = fb
        self.orchestrator = orchestrator
        self.backward = BackwardChainer(kb, fb)

    def root_cause_analysis(self, symptom: str, top_k: int = 3) -> str:
        """تحليل السبب الجذري لعرض أو مشكلة معينة"""
        report_lines = [f"🔍 تحليل السبب الجذري لـ: '{symptom}'\n"]
        
        # 1. البحث عن كل المتغيرات التي قد تسبب هذه الأعراض
        potential_causes = self.kb.find_affected_variables(symptom) if symptom in self.kb.causal_graph else set()
        # عكس الرسم للعثور على الآباء المحتملين
        ancestors = set()
        if symptom in self.kb.causal_graph:
            ancestors.update(nx.ancestors(self.kb.causal_graph, symptom))
            
        if not ancestors:
            report_lines.append("⚠️ لا توجد علاقات سببية مسجلة لهذه العاقبة في قاعدة المعرفة.")
            return "\n".join(report_lines)
            
        # 2. تقييم كل سبب محتمل
        candidates = []
        for cause in ancestors:
            proof = self.backward.prove(cause)
            conf = proof.confidence if proof.status == ProofStatus.PROVEN else 0.0
            candidates.append((cause, conf, proof))
            
        # ترتيب حسب اليقين
        candidates.sort(key=lambda x: x[1], reverse=True)
        
        report_lines.append("📊 الأسباب المحتملة مرتبة حسب درجة اليقين:")
        for i, (cause, conf, proof) in enumerate(candidates[:top_k], 1):
            report_lines.append(f"  {i}. {cause} (يقين: {conf:.2%})")
            if proof.rule_used:
                report_lines.append(f"     📏 القاعدة: {proof.rule_used}")
                
        report_lines.append("\n💡 التوصية: تحقق من العوامل ذات اليقين الأعلى أولاً.")
        return "\n".join(report_lines)

    def what_if_analysis(self, hypothetical_facts: Dict[str, bool]) -> str:
        """محاكاة تأثير إضافة حقائق افتراضية دون تغيير قاعدة الحقائق الفعلية"""
        report_lines = ["🧪 محاكاة ماذا لو:\n"]
        
        # إنشاء نسخة مؤقتة من قاعدة الحقائق
        temp_fb = copy.deepcopy(self.fb)
        for var, val in hypothetical_facts.items():
            temp_fb.add(var, val, TruthValue.TRUE, source="simulation", on_conflict='replace')
            
        # إعادة تشغيل الاستدلال على النسخة المؤقتة
        affected_vars = set()
        for var in hypothetical_facts:
            affected_vars.update(self.kb.find_affected_variables(var))
            
        if not affected_vars:
            report_lines.append("⚠️ لا توجد متغيرات متأثرة سببياً بهذه الفرضية.")
            return "\n".join(report_lines)
            
        report_lines.append("📈 المتغيرات المتأثرة وتغير احتمالاتها:")
        for var in affected_vars:
            result = self.orchestrator.infer(var, strategy=InferenceStrategy.SYMBOLIC_FIRST)
            if var in result:
                res = result[var]
                report_lines.append(f"  • {var}: {res.value} (يقين: {res.confidence:.2%})")
                
        report_lines.append("\n✅ المحاكاة اكتملت. لم يتم تغيير الحالة الفعلية للنظام.")
        return "\n".join(report_lines)

    def conflict_resolution_report(self) -> str:
        """كشف التناقضات الحالية واقتراح حلول"""
        report_lines = ["⚠️ تقرير التناقضات والمراجعات:\n"]
        conflicts = []
        for var, fact in self.fb.facts.items():
            if fact.truth == TruthValue.CONTRADICTED or fact.confidence < 0.4:
                conflicts.append((var, fact))
                
        if not conflicts:
            report_lines.append("✅ لا توجد تناقضات أو معتقدات ضعيفة حالياً.")
            return "\n".join(report_lines)
            
        for var, fact in conflicts:
            report_lines.append(f"  • {var}: قيمة={fact.value}, يقين={fact.confidence:.2%}, مصدر={fact.source}")
            report_lines.append(f"    💡 مقترح: مراجعة الأدلة المصدر أو تطبيق تحديث بيزي لرفع اليقين.")
            
        return "\n".join(report_lines)
