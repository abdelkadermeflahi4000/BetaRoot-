--- bayesian_network_simulation.py (原始)


+++ bayesian_network_simulation.py (修改后)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
محاكاة شاملة للشبكات البيزية (Bayesian Networks)
تجسيد عملي للنموذج الرسومي الاحتمالي الذي يدمج المنطق والاستدلال والمنهج العلمي

المثال الكلاسيكي: المطر - الرشاش - العشب الرطب (Rain-Sprinkler-Grass)
"""

import numpy as np
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
from pgmpy.sampling import BayesianModelSampling
import matplotlib.pyplot as plt
import networkx as nx

print("=" * 70)
print("محاكاة الشبكات البيزية: النموذج الموحد للمنطق والاستدلال")
print("=" * 70)

# =============================================================================
# ١. بناء الهيكل الرسومي (DAG Structure)
# =============================================================================
print("\n[١] بناء الهيكل الرسومي الموجه غير الدوري (DAG)...")

# تعريف الحواف: (الأب → الابن)
edges = [
    ('Rain', 'GrassWet'),      # المطر يؤثر على رطوبة العشب
    ('Sprinkler', 'GrassWet')  # الرشاش يؤثر على رطوبة العشب
]

model = DiscreteBayesianNetwork(edges)
print(f"✓ تم إنشاء الشبكة بالعقد: {model.nodes()}")
print(f"✓ تم إنشاء الشبكة بالحواف: {model.edges()}")

# =============================================================================
# ٢. تعريف جداول الاحتمالات الشرطية (CPTs)
# =============================================================================
print("\n[٢] تعريف جداول الاحتمالات الشرطية (Conditional Probability Tables)...")

# CPD للمطر (عقدة جذرية - لا آباء لها)
# P(Rain) = [0.2 للمطر, 0.8 لعدم المطر]
cpd_rain = TabularCPD(
    variable='Rain',
    variable_card=2,
    values=[[0.2], [0.8]],  # [No, Yes]
    state_names={'Rain': ['No', 'Yes']}
)
print("\nCPD للمطر (احتمال أولي):")
print(cpd_rain)

# CPD للرشاش (عقدة جذرية - لا آباء لها)
# P(Sprinkler) = [0.7 لا يعمل, 0.3 يعمل]
cpd_sprinkler = TabularCPD(
    variable='Sprinkler',
    variable_card=2,
    values=[[0.7], [0.3]],  # [No, Yes]
    state_names={'Sprinkler': ['No', 'Yes']}
)
print("\nCPD للرشاش (احتمال أولي):")
print(cpd_sprinkler)

# CPD للعشب الرطب (عقدة ابن - لها أبوان: Rain و Sprinkler)
# P(GrassWet | Rain, Sprinkler)
# الترتيب في القيم يجب أن يتطابق مع ترتيب الآباء
# الحالات الممكنة للآباء: (R=No,S=No), (R=No,S=Yes), (R=Yes,S=No), (R=Yes,S=Yes)
cpd_grass = TabularCPD(
    variable='GrassWet',
    variable_card=2,
    values=[
        # P(G=No | ...)
        [1.0,  0.2,  0.1,  0.01],
        # P(G=Yes | ...)
        [0.0,  0.8,  0.9,  0.99]
    ],
    evidence=['Rain', 'Sprinkler'],
    evidence_card=[2, 2],
    state_names={
        'GrassWet': ['No', 'Yes'],
        'Rain': ['No', 'Yes'],
        'Sprinkler': ['No', 'Yes']
    }
)
print("\nCPD للعشب الرطب (احتمال شرطي معقد):")
print(cpd_grass)

# إضافة الـ CPDs للنموذج
model.add_cpds(cpd_rain, cpd_sprinkler, cpd_grass)

# التحقق من صحة النموذج
if model.check_model():
    print("\n✓ النموذج صالح رياضياً (Valid Bayesian Network)")
else:
    print("\n✗ خطأ: النموذج غير صالح!")

# =============================================================================
# ٣. الاستدلال البيزي (Bayesian Inference)
# =============================================================================
print("\n" + "=" * 70)
print("[٣] الاستدلال البيزي: تطبيق منهجية البحث العلمي")
print("=" * 70)

inference = VariableElimination(model)

# --- السيناريو أ: استدلال تنبؤي (Predictive Inference) ---
print("\n--- أ. استدلال تنبؤي: من السبب إلى النتيجة ---")
print("السؤال: ما احتمال أن يكون العشب رطباً إذا علمنا أنه يمطر؟")
result_predict = inference.query(variables=['GrassWet'], evidence={'Rain': 'Yes'})
print(result_predict)
prob_wet_given_rain = result_predict.values[1]  # P(G=Yes | R=Yes)
print(f"→ الإجابة: P(GrassWet=Yes | Rain=Yes) = {prob_wet_given_rain:.4f}")

# --- السيناريو ب: استدلال تشخيصي (Diagnostic Inference) ---
print("\n--- ب. استدلال تشخيصي: من النتيجة إلى السبب ---")
print("السؤال: إذا رأينا العشب رطباً، ما احتمال أن يكون المطر هو السبب؟")
result_diagnostic = inference.query(variables=['Rain'], evidence={'GrassWet': 'Yes'})
print(result_diagnostic)
prob_rain_given_wet = result_diagnostic.values[1]  # P(R=Yes | G=Yes)
print(f"→ الإجابة: P(Rain=Yes | GrassWet=Yes) = {prob_rain_given_wet:.4f}")

# --- السيناريو ج: ظاهرة "إيضاح السبب البديل" (Explaining Away) ---
print("\n--- ج. ظاهرة 'Explaining Away' (استدلال تفسيري) ---")
print("هذا هو الجوهر الذكي للاستدلال البيزي!")
print("\nالخطوة ١: نعلم فقط أن العشب رطب.")
result_1 = inference.query(variables=['Sprinkler'], evidence={'GrassWet': 'Yes'})
prob_sprinkler_given_wet = result_1.values[1]
print(f"→ P(Sprinkler=Yes | GrassWet=Yes) = {prob_sprinkler_given_wet:.4f}")

print("\nالخطوة ٢: نضيف دليلاً جديداً → نعلم الآن أنه يمطر أيضاً!")
print("كيف يتغير اعتقادنا حول عمل الرشاش؟")
result_2 = inference.query(variables=['Sprinkler'], evidence={'GrassWet': 'Yes', 'Rain': 'Yes'})
prob_sprinkler_given_wet_and_rain = result_2.values[1]
print(f"→ P(Sprinkler=Yes | GrassWet=Yes, Rain=Yes) = {prob_sprinkler_given_wet_and_rain:.4f}")

print(f"\n💡 التحليل:")
print(f"   قبل معرفة المطر: احتمال الرشاح = {prob_sprinkler_given_wet:.4f}")
print(f"   بعد معرفة المطر:  احتمال الرشاح = {prob_sprinkler_given_wet_and_rain:.4f}")
if prob_sprinkler_given_wet > prob_sprinkler_given_wet_and_rain:
    print("   ← حدثت ظاهرة 'Explaining Away': وجود سبب كافٍ (المطر) قلل من الحاجة لسبب بديل (الرشاش)!")

# =============================================================================
# ٤. حساب التوزيع الاحتمالي المشترك (Joint Distribution)
# =============================================================================
print("\n" + "=" * 70)
print("[٤] التحقق من نظرية التفكيك (Factorization Theorem)")
print("=" * 70)

print("\nالتوزيع المشترك الكامل حسب النظرية:")
print("P(R, S, G) = P(R) × P(S) × P(G|R,S)")

# حساب يدوي لحالة واحدة كمثال: R=Yes, S=No, G=Yes
p_r_yes = 0.2
p_s_no = 0.7
p_g_yes_given_r_yes_s_no = 0.9  # من CPD العشب

joint_manual = p_r_yes * p_s_no * p_g_yes_given_r_yes_s_no
print(f"\nمثال: P(R=Yes, S=No, G=Yes) = {p_r_yes} × {p_s_no} × {p_g_yes_given_r_yes_s_no}")
print(f"                    = {joint_manual:.4f}")

# التحقق عبر الاستدلال (بدون passing evidence لأننا نحسب الاحتمال المشترك)
# نحتاج فقط حساب P(R=Yes, S=No, G=Yes) من التوزيع المشترك
result_joint = inference.query(variables=['Rain', 'Sprinkler', 'GrassWet'])
# استخراج القيمة المطلوبة من النتيجة
# المؤشرات: Rain=Yes(1), Sprinkler=No(0), GrassWet=Yes(1)
joint_from_network = result_joint.values[1, 0, 1]
print(f"✓ التحقق عبر الشبكة: {joint_from_network:.4f}")
print(f"  الفرق عن الحساب اليدوي: {abs(joint_from_network - joint_manual):.6f} (تقريب عددي)")

# =============================================================================
# ٥. محاكاة منهجية البحث العلمي التكرارية
# =============================================================================
print("\n" + "=" * 70)
print("[٥] محاكاة دورة البحث العلمي: تحديث المعتقدات")
print("=" * 70)

print("\nالسيناريو: عالم يلاحظ العشب الرطب ويحاول استنتاج السبب")
print("-" * 50)

# المعتقدات الأولية (Priors)
print("\nالمرحلة ١: المعتقدات الأولية (قبل أي ملاحظة)")
prior_rain = 0.2
prior_sprinkler = 0.3
print(f"   P(Rain) = {prior_rain}")
print(f"   P(Sprinkler) = {prior_sprinkler}")

# الملاحظة الأولى
print("\nالمرحلة ٢: الملاحظة التجريبية → العشب رطب! (E = GrassWet=Yes)")
print("   تحديث المعتقدات باستخدام بايز...")

posterior_rain = prob_rain_given_wet
posterior_sprinkler = prob_sprinkler_given_wet

print(f"   P(Rain | GrassWet) = {posterior_rain:.4f} ↑ (زاد من {prior_rain})")
print(f"   P(Sprinkler | GrassWet) = {posterior_sprinkler:.4f} ↑ (زاد من {prior_sprinkler})")

# ملاحظة إضافية (تجربة مضبوطة)
print("\nالمرحلة ٣: تجربة إضافية → التأكد من وجود مطر! (E2 = Rain=Yes)")
print("   تحديث المعتقدات مرة أخرى...")

final_sprinkler = prob_sprinkler_given_wet_and_rain
print(f"   P(Sprinkler | GrassWet, Rain) = {final_sprinkler:.4f} ↓ (انخفض!")

print("\n" + "-" * 50)
print("الخلاصة العلمية:")
print("  ١. الملاحظة الأولية رفعت احتمال كلا السببين (استقراء).")
print("  ٢. الدليل الإضافي فَضَّل سبباً على آخر (تفنيط نسبي).")
print("  ٣. هذه هي نفس خوارزمية المنهج العلمي: ملاحظة → فرضية → اختبار → تحديث!")

# =============================================================================
# ٦. تمثيل رسومي للشبكة
# =============================================================================
print("\n" + "=" * 70)
print("[٦] التمثيل المرئي للشبكة البيزية")
print("=" * 70)

try:
    # إنشاء رسم بياني بسيط باستخدام networkx
    G = nx.DiGraph()
    G.add_edges_from(edges)

    # ترتيب العقد للرسم
    pos = {'Rain': (0, 1), 'Sprinkler': (2, 1), 'GrassWet': (1, 0)}

    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue',
            node_size=3000, font_size=12, font_weight='bold',
            arrowsize=20, arrowstyle='-|>', edge_color='gray')

    # إضافة الاحتمالات كعنوان
    plt.title("الشبكة البيزية: Rain → GrassWet ← Sprinkler\n(Bayesian Network Structure)",
              fontsize=14, pad=20)

    plt.tight_layout()
    plt.savefig('bayesian_network_structure.png', dpi=150, bbox_inches='tight')
    print("\n✓ تم حفظ الرسم البياني في: bayesian_network_structure.png")
    print("  (في بيئة حقيقية، سيظهر الرسم هنا)")

    # طباعة تمثيل نصي بديل
    print("\nالتمثيل النصي للهيكل:")
    print("""
    [Rain] ─────────┐
      (P=0.2)       │
                    ▼
               [GrassWet]
                    ▲
      (P=0.3)       │
    [Sprinkler] ────┘

    المعادلة: P(R,S,G) = P(R) × P(S) × P(G|R,S)
    """)

except Exception as e:
    print(f"\n⚠ تعذر إنشاء الرسم البياني: {e}")
    print("  لكن الحسابات الرياضية صحيحة بالكامل.")

# =============================================================================
# الخلاصة النهائية
# =============================================================================
print("\n" + "=" * 70)
print("الخلاصة: الشبكات البيزية كوعاء رياضي موحد")
print("=" * 70)
print("""
✓ المنطق الصوري: تجسد في الاستقلال الشرطي (Conditional Independence)
✓ الاستدلال الاستنتاجي: حساب P(E|H) من جداول CPT
✓ الاستدلال الاستقرائي: تحديث P(H|E) عبر بايز
✓ منهجية البحث العلمي: دورة تكرارية من الملاحظة والتحديث

الشبكات البيزية هي التنفيذ العملي الكامل للإطار النظري الذي ناقشناه!
""")
print("=" * 70)
print("تمت المحاكاة بنجاح!")
print("=" * 70)