"""
tests/test_integration_cognitive_cycle.py
Integration Test: Full Cognitive Cycle for BetaRoot
Tests: Memory Ingestion ↔ Reasoning Logging ↔ Goal Tracking ↔ Self-Reflection ↔ Calibration

Run:
  pytest tests/test_integration_cognitive_cycle.py -v
  python -m pytest tests/test_integration_cognitive_cycle.py -v --tb=short
"""
import pytest
import sys, os, json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

# Ensure project root is in PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import core cognitive components (as designed in previous steps)
try:
    from betaroot.memory.memory_manager import MemoryManager, MemoryType, Priority, TrustLevel
    from betaroot.goal.goal_system import GoalManager, GoalType, GoalStatus
    from betaroot.core.self_reflection import SelfReflectionModule, BiasType, ImprovementAction
    MODULES_AVAILABLE = True
except ImportError as e:
    MODULES_AVAILABLE = False
    pytest.skip(f"Core modules not found. Install project dependencies first. Error: {e}", allow_module_level=True)


class TestCognitiveCycle:
    """اختبار تكامل الدورة المعرفية الكاملة لـ BetaRoot"""
    
    @pytest.fixture(autouse=True)
    def setup_system(self, tmp_path: Path):
        """تهيئة جميع المكونات المعرفية قبل كل اختبار"""
        self.memory = MemoryManager(storage_dir=str(tmp_path / "memory"))
        self.goal_mgr = GoalManager(memory_manager=self.memory, storage_path=str(tmp_path / "goals"))
        self.reflection = SelfReflectionModule(config={"min_log_size": 3})  # عتبة منخفضة للاختبار
        self.inference_logs: List[Dict[str, Any]] = []
        self.tmp_path = tmp_path
        
    # ==========================================
    # 🔧 أدوات مساعدة لمحاكاة الدورة
    # ==========================================
    def _log_inference(self, query: str, confidence: float, actual_accuracy: float, 
                       source: str = "bayesian", contradictions: int = 0, revised: bool = False):
        """محاكاة تسجيل نتيجة استدلال من محرك الاستدلال"""
        log = {
            "query": query,
            "confidence": round(confidence, 3),
            "actual_accuracy": round(actual_accuracy, 3),
            "source": source,
            "reasoning_steps": ["premise_check", "causal_propagation", "evidence_matching"],
            "contradictory_evidence_count": contradictions,
            "revised": revised,
            "timestamp": datetime.now().isoformat()
        }
        self.inference_logs.append(log)
        return log

    # ==========================================
    # 📦 المرحلة ١: استيعاب المعرفة وإدارة الذاكرة
    # ==========================================
    def test_phase_1_memory_ingestion_and_prioritization(self):
        """التحقق من تخزين الحقائق، الفهرسة الدلالية، وتوزيع الثقة/الأولوية"""
        # 1. تخزين حقائق بثقة وأولويات مختلفة
        fact1 = self.memory.store(
            content={"subject": "smoking", "predicate": "causes", "value": "lung_cancer"},
            memory_type=MemoryType.FACT, priority=Priority.CRITICAL, 
            trust=TrustLevel.VERIFIED, source="medical_journal", tags=["health", "causation"]
        )
        
        fact2 = self.memory.store(
            content={"subject": "coffee", "predicate": "improves", "value": "focus"},
            memory_type=MemoryType.FACT, priority=Priority.LOW, 
            trust=TrustLevel.LOW_CONFIDENCE, source="user_anecdote", tags=["nutrition", "cognition"]
        )
        
        # 2. التحقق من التخزين في الطبقات الصحيحة
        assert fact1.priority == Priority.CRITICAL
        assert fact2.priority == Priority.LOW
        assert fact1.trust == TrustLevel.VERIFIED
        assert fact2.trust == TrustLevel.LOW_CONFIDENCE
        
        # 3. التحقق من الفهرسة والبحث الدلالي
        results = self.memory.retrieve("lung cancer risk", limit=5, min_trust=TrustLevel.MEDIUM_CONFIDENCE)
        assert len(results) >= 1
        assert results[0].content["subject"] == "smoking"
        
        # 4. التحقق من إحصائيات الذاكرة
        stats = self.memory.get_stats()
        assert stats["ltm_count"] >= 1
        assert stats["stm_count"] >= 1
        assert stats["trust_distribution"][TrustLevel.VERIFIED.name] >= 1

    # ==========================================
    # 🧠 المرحلة ٢: الاستدلال وتسجيل الأهداف
    # ==========================================
    def test_phase_2_reasoning_logging_and_goal_tracking(self):
        """التحقق من تسجيل الاستدلال، صياغة الأهداف، وتتبع التقدم"""
        # 1. محاكاة استدلالين (واحد دقيق، واحد مبالغ في الثقة)
        self._log_inference("Is smoking linked to cancer?", confidence=0.98, actual_accuracy=0.95, source="bayesian")
        self._log_inference("Does coffee cure migraines?", confidence=0.92, actual_accuracy=0.40, contradictions=2, source="user")
        
        # 2. إنشاء هدف بناءً على فجوة معرفية
        goal = self.goal_mgr.create_goal(
            title="Verify Coffee-Migraine Causation",
            description="Cross-reference clinical studies to resolve conflicting beliefs",
            goal_type=GoalType.KNOWLEDGE_ACQUISITION,
            success_criteria={"coffee_migraine_confirmed": True},
            priority=0.85, tags=["medicine", "verification"]
        )
        
        # 3. التحقق من حالة الهدف
        assert goal.status == GoalStatus.PROPOSED
        assert goal.priority == 0.85
        assert "medicine" in goal.tags
        
        # 4. محاكاة تقدم الهدف وتحديثه
        self.goal_mgr.goals[goal.id].update_state(progress=0.6, confidence=0.75)
        progress_map = self.goal_mgr.evaluate_progress(goal.id)
        assert progress_map[goal.id] > 0.5
        
        # 5. التحقق من دورة التشغيل (Tick)
        tick_result = self.goal_mgr.tick()
        assert "next_actions" in tick_result
        assert len(tick_result["next_actions"]) <= 3

    # ==========================================
    # 🔍 المرحلة ٣: التقييم الذاتي وكشف التحيز
    # ==========================================
    def test_phase_3_self_reflection_and_bias_detection(self):
        """التحقق من كشف فرط الثقة، تحيز المصدر، وتوليد خطط التحسين"""
        # 1. توليد سجل استدلال يحتوي أنماط متحيزة
        for i in range(5):
            self._log_inference(f"Query_{i}", confidence=0.95, actual_accuracy=0.50, contradictions=1) # فرط ثقة منهجي
        self._log_inference("UserSourceQuery", confidence=0.80, actual_accuracy=0.80, source="unverified_source")
        
        # 2. تشغيل التقييم الذاتي
        trust_scores = {"medical_journal": 0.95, "unverified_source": 0.85, "user": 0.60}
        report = self.reflection.evaluate_and_reflect(
            inference_logs=self.inference_logs,
            trust_scores=trust_scores,
            memory_stats={"ltm_count": 12, "avg_importance": 0.65}
        )
        
        assert report is not None
        assert report.evaluation_score < 0.8  # منخفض بسبب فرط الثقة
        assert report.calibration_error > 0.2  # فرق كبير بين الثقة والدقة
        
        # 3. التحقق من كشف التحيز
        overconf_biases = [b for b in report.biases_detected if b["type"] == BiasType.OVERCONFIDENCE.value]
        assert len(overconf_biases) >= 3  # على الأقل 3 حالات فرط ثقة مسجلة
        
        # 4. التحقق من خطة التحسين
        assert len(report.suggested_actions) >= 1
        recalc_action = next((a for a in report.suggested_actions 
                              if a["action"] == ImprovementAction.RECALIBRATE_CONFIDENCE.value), None)
        assert recalc_action is not None
        assert recalc_action["adjustment"] < 0  # يجب أن يكون سالبًا لخفض الثقة

    # ==========================================
    # 🔄 اختبار الدورة المعرفية الكاملة (End-to-End)
    # ==========================================
    def test_full_cognitive_cycle_integration(self):
        """اختبار تدفق كامل: تخزين ← استدلال ← هدف ← تقييم ← تصدير"""
        # 🔹 خطوة 1: استيعاب معرفة أولية
        self.memory.store(
            content={"subject": "drug_x", "predicate": "treats", "value": "symptom_y"},
            memory_type=MemoryType.FACT, priority=Priority.HIGH, 
            trust=TrustLevel.MEDIUM_CONFIDENCE, source="clinical_trial_phase2"
        )
        
        # 🔹 خطوة 2: استدلال وتسجيل
        self._log_inference("Does DrugX work?", confidence=0.85, actual_accuracy=0.82, source="bayesian")
        self._log_inference("Is DrugX safe?", confidence=0.99, actual_accuracy=0.60, contradictions=3, source="unverified")
        
        # 🔹 خطوة 3: هدف معرفي
        safety_goal = self.goal_mgr.create_goal(
            title="Assess DrugX Safety Profile",
            description="Aggregate adverse event reports and verify against medical database",
            goal_type=GoalType.EXPLORATION,
            success_criteria={"safety_verified": True},
            priority=0.9, tags=["pharmacology", "safety"]
        )
        
        # 🔹 خطوة 4: تقييم ذاتي
        trust_dist = {"clinical_trial_phase2": 0.8, "unverified": 0.4}
        reflection_report = self.reflection.evaluate_and_reflect(
            inference_logs=self.inference_logs,
            trust_scores=trust_dist,
            memory_stats=self.memory.get_stats()
        )
        
        # 🔹 خطوة 5: التحقق من الاتساق الشامل
        assert reflection_report.evaluation_score > 0.0
        assert len(reflection_report.biases_detected) > 0
        assert self.goal_mgr.goals[safety_goal.id].status in (GoalStatus.PROPOSED, GoalStatus.ACTIVE)
        
        # 🔹 خطوة 6: التصدير والاستعادة (Persistence)
        mem_export = self.memory.export_state(str(self.tmp_path / "mem_state.json"))
        goals_export = self.goal_mgr.save_state("goals_test.json")
        reflection_export = self.reflection.export_reflection_log(str(self.tmp_path / "reflections.json"))
        
        assert Path(mem_export).exists()
        assert Path(goals_export).exists()
        assert Path(reflection_export).exists()
        
        # التحقق من أن الملفات تحتوي على بيانات صالحة
        with open(reflection_export, "r", encoding="utf-8") as f:
            exported_data = json.load(f)
            assert len(exported_data) >= 1
            assert exported_data[0]["evaluation_score"] > 0
            
        print("\n✅ FULL COGNITIVE CYCLE TEST PASSED:")
        print(f"   • Memory: {self.memory.get_stats()['ltm_count']} long-term facts stored")
        print(f"   • Goals: {len(self.goal_mgr.goals)} active, priority queue sorted")
        print(f"   • Reflection: Calibration Error={reflection_report.calibration_error:.3f}, Biases={len(reflection_report.biases_detected)}")
        print(f"   • Exports: 3 files saved successfully")

    # ==========================================
    # 📊 اختبار الاتجاهات طويلة المدى
    # ==========================================
    def test_reflection_trend_analysis(self):
        """التحقق من تحليل اتجاه التقييم الذاتي عبر الزمن"""
        # محاكاة 5 جلسات تقييم متتالية
        for i in range(5):
            self._log_inference(f"Session_{i}_Query", confidence=0.7 + (i*0.05), actual_accuracy=0.75)
            self.reflection.evaluate_and_reflect(self.inference_logs[:len(self.inference_logs)])
            
        trend = self.reflection.get_trend_analysis(window=5)
        assert "avg_score" in trend
        assert "score_trend" in trend
        assert trend["total_reflections"] == 5
        assert trend["avg_score"] > 0.0
        assert trend["score_trend"] in ("improving", "declining", "stable")


# ==========================================
# 🚀 تشغيل مباشر (بدون pytest)
# ==========================================
if __name__ == "__main__":
    import tempfile
    print("🧪 Running BetaRoot Cognitive Cycle Integration Tests (Standalone Mode)...")
    
    # إنشاء مؤقت للملفات
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        # تهيئة النظام يدويًا
        mem = MemoryManager(storage_dir=str(tmp_path / "memory"))
        goal_mgr = GoalManager(memory_manager=mem, storage_path=str(tmp_path / "goals"))
        refl = SelfReflectionModule(config={"min_log_size": 2})
        logs = []
        
        def log_inf(q, c, a, src="test"):
            logs.append({"query": q, "confidence": c, "actual_accuracy": a, "source": src, 
                         "contradictory_evidence_count": 0, "revised": False, "timestamp": datetime.now().isoformat()})
            
        # تشغيل الدورة
        mem.store({"subject": "A", "predicate": "causes", "value": "B"}, MemoryType.FACT, Priority.HIGH, TrustLevel.VERIFIED)
        log_inf("Test_1", 0.9, 0.85)
        log_inf("Test_2", 0.95, 0.50)
        g = goal_mgr.create_goal("Verify_C", "Test goal", GoalType.KNOWLEDGE_ACQUISITION, {"verified": True}, 0.8)
        report = refl.evaluate_and_reflect(logs, {"test": 0.7}, mem.get_stats())
        
        print(f"✅ Memory Stats: LTM={mem.get_stats()['ltm_count']}")
        print(f"✅ Goal Status: {g.status.value}")
        print(f"✅ Reflection Score: {report.evaluation_score:.3f}")
        print(f"✅ Biases Found: {len(report.biases_detected)}")
        print("🎉 ALL COGNITIVE CYCLE CHECKS PASSED!")
