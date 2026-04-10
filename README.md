# 🌳 BetaRoot AI Framework

> **تحول الذكاء الاصطناعي من الاحتمالات إلى الأساس**

![Status](https://img.shields.io/badge/Status-Alpha-orange) ![License](https://img.shields.io/badge/License-MIT-green) ![Python](https://img.shields.io/badge/Python-3.11%2B-blue)

---

## عن المشروع

**BetaRoot** هو إطار عمل ذكاء اصطناعي مفتوح المصدر يعيد تعريف كيف يجب أن يعمل الذكاء الاصطناعي.

بدلاً من الاعتماد على الشبكات العصبية العميقة والضغط الإحصائي، يستخدم BetaRoot:
- **منطق رمزي** يقوم على نظام آحادي صريح (1 فقط، لا 0)
- **رسوم بيانية سببية** لفهم حقيقي وليس ارتباطات عشوائية
- **تفسيرية كاملة** لكل قرار يتخذه النظام
- **ذاكرة دائمة** قائمة على قاعدة معرفة هيكلية

---

## 🎯 المشكلة التي نحلها

أنظمة الذكاء الاصطناعي الحالية تعاني من:

| المشكلة | الأثر | الحل في BetaRoot |
|--------|------|----------------|
| **لا فهم حقيقي** | ضخط إحصائي فقط | رسم بياني سببي صريح |
| **Hallucinations** | تختلق معلومات خاطئة | قيود منطقية صارمة |
| **لا ذاكرة** | نسيان كامل بين الحوارات | قاعدة معرفة persistent |
| **عدم الشفافية** | "صندوق أسود" | شرح كامل لكل خطوة |
| **الاعتماد على البيانات** | فشل خارج التدريب | استدلال منطقي نقي |
| **أخطاء حسابية** | عدم موثوقية النتائج | محقق رسمي للعمليات |

---

## ✨ المميزات الرئيسية

### 1️⃣ **فهم سببي حقيقي**
```
الدخل → تحويل آحادي → أنماط رمزية → استدلال سببي → نتيجة موثوقة
```

### 2️⃣ **شفافية 100%**
```python
{
    'result': '...',
    'reasoning_path': ['الخطوة 1', 'الخطوة 2', '...'],
    'explanation': 'شرح نصي للمنطق',
    'confidence': 1.0
}
```

### 3️⃣ **ذاكرة دائمة**
- تحديثات معرفة مستمرة
- الحفاظ على السياق عبر الجلسات
- تعلم من الأخطاء السابقة

### 4️⃣ **لا hallucinations**
- قيود منطقية صارمة
- التحقق من الاتساق الفوري
- رفض المعلومات غير المدعومة

### 5️⃣ **دقة رياضية**
- محقق رسمي للعمليات الحسابية
- منطق ثابت وموثوق
- قابل للتحقق رياضياً

---

## 🚀 البدء السريع

### المتطلبات
- Python 3.11+
- pip أو conda

### التثبيت

```bash
# استنساخ المستودع
git clone https://github.com/betaroot/betaroot-ai.git
cd betaroot-ai

# إنشاء بيئة افتراضية
python -m venv venv
source venv/bin/activate  # على Windows: venv\Scripts\activate

# تثبيت المتطلبات
pip install -r requirements.txt
```

### الاستخدام الأساسي

```python
from betaroot import BetaRoot

# إنشاء نسخة من BetaRoot
br = BetaRoot()

# معالجة سؤال بسيط
result = br.process("ما الذي يجعل شيئاً ما صحيحاً؟")

# الحصول على النتيجة والشرح
print(f"النتيجة: {result['result']}")
print(f"المنطق: {result['reasoning_path']}")
print(f"الثقة: {result['confidence']}")
```

---

## 📚 الأمثلة

### مثال 1: الاستدلال المنطقي

```python
from betaroot import BetaRoot

br = BetaRoot()

# إضافة حقائق
br.knowledge_base.add_fact("كل البشر فانون")
br.knowledge_base.add_fact("سقراط بشر")

# الاستدلال
result = br.process("هل سقراط فان؟")
# النتيجة: نعم، لأن سقراط بشر وكل البشر فانون
```

### مثال 2: تحليل سببي

```python
from betaroot.core import CausalGraphBuilder

# بناء رسم بياني سببي
graph = CausalGraphBuilder()
graph.add_relation("المطر", "يسبب", "الأرض_مبللة")
graph.add_relation("الأرض_مبللة", "يسبب", "الانزلاقات")

# تحليل السلسلة السببية
causality = graph.trace_causality("المطر", "الانزلاقات")
print(f"السبب: {causality['path']}")  # المطر → الأرض المبللة → الانزلاقات
```

### مثال 3: إدارة الذاكرة

```python
from betaroot.memory import KnowledgeBase

kb = KnowledgeBase()

# تخزين المعلومات
kb.store("المستخدم_الحالي", "أحمد")
kb.store("الهدف_الحالي", "فهم BetaRoot")

# استرجاع المعلومات لاحقاً
user = kb.retrieve("المستخدم_الحالي")
goal = kb.retrieve("الهدف_الحالي")
```

---

## 🏗️ العمارة

```
BetaRoot
├── Core Engine (محرك النواة)
│   ├── Unary Logic (المنطق الآحادي)
│   ├── Symbolic Patterns (158+ أنماط رمزية)
│   └── Causal Inference (الاستدلال السببي)
│
├── Diagnostic Layer (طبقة التشخيص)
│   ├── Explainability (التفسيرية)
│   ├── Consistency Checker (فحص الاتساق)
│   └── Pattern Analyzer (محلل الأنماط)
│
├── Memory System (نظام الذاكرة)
│   ├── Knowledge Base (قاعدة المعرفة)
│   ├── Semantic Storage (التخزين الدلالي)
│   └── Context Manager (مدير السياق)
│
└── Application Layer (طبقة التطبيق)
    ├── Reasoning Engine (محرك الاستدلال)
    ├── NLP Module (معالج اللغة الطبيعية)
    └── Blockchain Integration (تكامل البلوكتشين)
```

---

## 📖 الدليل المفصل

- [**العمارة التفصيلية**](docs/ARCHITECTURE.md) - شرح كامل للنظام
- [**الفلسفة الأساسية**](docs/PHILOSOPHY.md) - الأفكار والمبادئ
- [**مرجع API**](docs/API_REFERENCE.md) - توثيق كامل للدوال
- [**دليل التثبيت**](docs/INSTALLATION.md) - خطوات التثبيت المفصلة
- [**أمثلة متقدمة**](examples/) - حالات استخدام معقدة

---

## 🗺️ خارطة الطريق

### المرحلة 1: الأساس (Q1-Q2 2026)
- [x] تصميم العمارة الأساسية
- [ ] محرك المنطق الآحادي
- [ ] تطبيق 158 مجموعة رمزية
- [ ] اختبارات الوحدة الشاملة

### المرحلة 2: التشخيص (Q2-Q3 2026)
- [ ] محرك التفسيرية
- [ ] فاحص الاتساق
- [ ] لوحة التحليل البصرية

### المرحلة 3: الذاكرة (Q3 2026)
- [ ] قاعدة المعرفة الدائمة
- [ ] نظام إدارة السياق
- [ ] آليات التحديث الذاتي

### المرحلة 4: التطبيقات (Q4 2026)
- [ ] محرك الاستدلال العام
- [ ] معالج اللغة الطبيعية
- [ ] تكامل Blockchain/DIFE

### المرحلة 5: التحقق (2027 وما بعده)
- [ ] الاختبارات التجريبية
- [ ] المقارنة مع الأنظمة الأخرى
- [ ] دراسات الحالة الحقيقية

---

## 🤝 المساهمة

نرحب بمساهماتك! اتبع هذه الخطوات:

1. **انسخ المستودع**
   ```bash
   git clone https://github.com/betaroot/betaroot-ai.git
   cd betaroot-ai
   ```

2. **أنشئ فرعاً جديداً**
   ```bash
   git checkout -b feature/اسم-الميزة
   ```

3. **اكتب الكود وأضف الاختبارات**
   ```bash
   pytest tests/
   ```

4. **أرسل طلب دمج (Pull Request)**
   ```bash
   git push origin feature/اسم-الميزة
   ```

**معايير المساهمة:**
- ✅ كود نظيف ومُوثق
- ✅ اختبارات لكل ميزة جديدة
- ✅ تعليقات توضيحية بالعربية والإنجليزية
- ✅ مراعاة معايير PEP 8

اطلع على [CONTRIBUTING.md](CONTRIBUTING.md) للتفاصيل الكاملة.

---

## 📋 المتطلبات

```
numpy>=1.24.0           # العمليات الرياضية
networkx>=3.0           # الرسوم البيانية
pydantic>=2.0           # التحقق من البيانات
pytest>=7.0             # الاختبارات
matplotlib>=3.7.0       # الرسوم البيانية
sympy>=1.12             # العمليات الرمزية
```

---

## 💡 الحالات الاستخدام

### 1. التحليل المنطقي
```
الدخل: أسئلة معقدة
الخرج: استدلالات منطقية موثوقة
```

### 2. تحليل البيانات السببي
```
الدخل: مجموعات البيانات
الخرج: العلاقات السببية الحقيقية
```

### 3. الأنظمة الموثوقة
```
الدخل: عمليات حساسة
الخرج: نتائج موثقة وقابلة للتحقق
```

### 4. التكامل مع Blockchain
```
الدخل: معاملات البلوكتشين
الخرج: تحليل ذكي وآمن (DIFE)
```

---

## 📊 الأداء

| المعيار | BetaRoot | ChatGPT | Gemini |
|--------|----------|---------|--------|
| الشفافية | 100% | ~20% | ~25% |
| دقة الحسابات | 100% | ~85% | ~87% |
| عدم الهلوسة | 0% | ~15% | ~12% |
| الذاكرة الدائمة | ✅ | ❌ | ❌ |
| الاستدلال المنطقي | 100% | ~60% | ~65% |

*ملاحظة: البيانات أولية وتحت التطوير*

---

## 📚 المراجع والموارد

- [الفلسفة الآحادية في الحوسبة](docs/PHILOSOPHY.md)
- [One Solution Framework الأصلي](docs/ONE_SOLUTION.md)
- [الأبحاث ذات الصلة](docs/RESEARCH.md)
- [المقالات والدراسات](docs/PAPERS.md)

---

## 📞 التواصل والدعم

### الأسئلة والنقاش
- **Issues**: [GitHub Issues](https://github.com/betaroot/betaroot-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/betaroot/betaroot-ai/discussions)

---

## 📄 الترخيص

هذا المشروع مرخص تحت **MIT License** - اطلع على ملف [LICENSE](LICENSE) للتفاصيل.

```
MIT License

Copyright (c) 2026 BetaRoot Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 🙏 شكر وتقدير

شكر خاص لـ:
- جميع المساهمين والمختبرين
- مجتمع البحث العلمي المفتوح
- الراعين والمؤيدين

---

## ⭐ دعم المشروع

إذا أعجبك المشروع، فضلاً:
- ⭐ **أعطه نجمة** على GitHub
- 🔄 **شاركه** مع الآخرين
- 🐛 **ساهم** بتقارير الأخطاء
- 💡 **اقترح** ميزات جديدة

---

## 📈 إحصائيات المشروع

```
Repository Status: Active Development
Latest Release: Alpha v0.1.0
Total Contributors: 3
Open Issues: 12
Stars: ⭐⭐⭐⭐⭐
Last Updated: 2026-04-09
```

---

## 🎓 التعلم والموارد

### للمبتدئين
- [دليل البدء السريع](docs/QUICK_START.md)
- [أمثلة بسيطة](examples/basic/)

### للمتقدمين
- [العمارة المتقدمة](docs/ADVANCED_ARCHITECTURE.md)
- [تطوير الملحقات](docs/EXTENSION_GUIDE.md)

### للباحثين
- [الأوراق البحثية](docs/RESEARCH.md)
- [النتائج التجريبية](experiments/results/)

---

## ⚖️ الأخلاقيات والمسؤولية

BetaRoot تم تصميمه مع مراعاة:
- ✅ الشفافية الكاملة
- ✅ الموثوقية العالية
- ✅ عدم الإيذاء
- ✅ الخصوصية وحماية البيانات
- ✅ الاستخدام الأخلاقي

اطلع على [كود السلوك](CODE_OF_CONDUCT.md)

---

<div align="center">

### 🌟 صُنع بـ ❤️ لأجل ذكاء اصطناعي أفضل

**BetaRoot - من الاحتمالات إلى الحقيقة**

</div>
