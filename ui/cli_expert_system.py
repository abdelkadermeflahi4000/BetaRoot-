# betaroot/ui/cli_expert_system.py
import sys
from typing import Dict, Optional
from ..core.knowledge import KnowledgeBase, FactBase, TruthValue
from ..core.inference.orchestrator import InferenceOrchestrator, InferenceStrategy
from ..core.analysis.diagnostic_analyzer import DiagnosticAnalyzer

class ExpertSystemCLI:
    """
    واجهة مستخدم تفاعلية بسيطة لنظام الخبراء
    مصممة لغير الخبراء، مع توجيه ذكي ودعم اللغتين
    """
    def __init__(self, kb: KnowledgeBase, fb: FactBase, orchestrator: InferenceOrchestrator):
        self.kb = kb
        self.fb = fb
        self.orchestrator = orchestrator
        self.analyzer = DiagnosticAnalyzer(kb, fb, orchestrator)
        self.current_domain = "default"

    def run(self):
        print("🤖 مرحباً بك في نظام BetaRoot الخبير")
        print("💡 اكتب 'help' للأوامر، 'exit' للخروج\n")
        
        while True:
            try:
                cmd = input("👤 المستخدم> ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\n👋 انتهاء الجلسة.")
                break
                
            if cmd in ('exit', 'quit', 'خروج'):
                print("✅ تم حفظ الجلسة بنجاح.")
                break
            elif cmd == 'help':
                self._show_help()
            elif cmd.startswith('add ') or cmd.startswith('أضف '):
                self._handle_add_facts(cmd)
            elif cmd.startswith('ask ') or cmd.startswith('اسأل '):
                self._handle_ask_query(cmd)
            elif cmd.startswith('diagnose ') or cmd.startswith('شخّص '):
                self._handle_diagnose(cmd)
            elif cmd.startswith('whatif ') or cmd.startswith('ماذا_لو '):
                self._handle_what_if(cmd)
            elif cmd in ('explain', 'شرح'):
                self._show_explanation()
            elif cmd in ('status', 'حالة'):
                self._show_status()
            else:
                print("⚠️ أمر غير معروف. اكتب 'help' لعرض الخيارات.")

    def _show_help(self):
        print("\n📖 الأوامر المدعومة:")
        print("  add / أضف <variable> <value> [confidence]  → إضافة حقيقة جديدة")
        print("  ask / اسأل <hypothesis>                    → استفسار عن احتمال أو نتيجة")
        print("  diagnose / شخّص <symptom>                  → تحليل سببي شامل")
        print("  whatif / ماذا_لو <var1=val1, var2=val2>    → محاكاة افتراضية")
        print("  explain / شرح                              → عرض آخر استنتاج مع التبرير")
        print("  status / حالة                              → عرض حالة النظام الحالية")
        print("  exit / خروج                                → إنهاء الجلسة\n")

    def _handle_add_facts(self, cmd: str):
        parts = cmd.split()
        if len(parts) < 3:
            print("❌ الاستخدام: add <variable> <value> [confidence]")
            return
        var, val = parts[1], parts[2]
        conf = float(parts[3]) if len(parts) > 3 else 1.0
        success, msg = self.fb.add(var, val == 'true' or val == '1', TruthValue.TRUE, conf, "user")
        print(f"{'✅' if success else '⚠️'} {msg}" if success else f"❌ {msg}")

    def _handle_ask_query(self, cmd: str):
        hypothesis = cmd.split(' ', 1)[1] if ' ' in cmd else None
        if not hypothesis:
            print("❌ الاستخدام: ask <hypothesis>")
            return
        results = self.orchestrator.infer(hypothesis, strategy=InferenceStrategy.SYMBOLIC_FIRST)
        res = results.get(hypothesis)
        if res:
            print(f"\n📊 النتيجة:")
            print(f"  • الفرضية: {hypothesis}")
            print(f"  • القيمة: {res.value}")
            print(f"  • درجة اليقين: {res.confidence:.2%}")
            print(f"  • الطريقة المستخدمة: {res.method}")
        else:
            print("❌ لا يوجد استنتاج حالياً لهذه الفرضية.")

    def _handle_diagnose(self, cmd: str):
        symptom = cmd.split(' ', 1)[1] if ' ' in cmd else None
        if not symptom:
            print("❌ الاستخدام: diagnose <symptom>")
            return
        report = self.analyzer.root_cause_analysis(symptom)
        print(f"\n🔍 تقرير التحليل التشخيصي:\n{report}")

    def _handle_what_if(self, cmd: str):
        try:
            raw = cmd.split(' ', 1)[1]
            hypothetical = {k: v=='true' or v=='1' for k,v in (item.split('=') for item in raw.split(','))}
            report = self.analyzer.what_if_analysis(hypothetical)
            print(f"\n🧪 محاكاة ماذا لو:\n{report}")
        except Exception as e:
            print(f"❌ خطأ في الصيغة: {e}")

    def _show_explanation(self):
        print("📜 آخر استنتاجات الجلسة:")
        for entry in self.fb.get_history(limit=5):
            print(f"  • [{entry.timestamp.strftime('%H:%M:%S')}] {entry.variable} ← {entry.action}")

    def _show_status(self):
        print(f"\n📊 حالة النظام:")
        print(f"  • القواعد المحملة: {len(self.kb)}")
        print(f"  • الحقائق النشطة: {len(self.fb)}")
        print(f"  • التناقضات المكتشفة: {len(self.fb.detect_conflicts({}))}")
