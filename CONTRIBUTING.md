# 🤝 Contributing to BetaRoot

## العربية

---

## دليل المساهمة

شكراً لاهتمامك بالمساهمة في BetaRoot! هذا المستند يوضح كيفية المساهمة بفعالية.

### المتطلبات الأساسية

قبل البدء، تأكد من:
- ✅ لديك حساب GitHub
- ✅ مثبت Python 3.11 أو أحدث
- ✅ مثبت Git
- ✅ اطلعت على [PHILOSOPHY.md](docs/PHILOSOPHY.md)

### خطوات البدء

#### 1. استنساخ المستودع

```bash
git clone https://github.com/betaroot/betaroot-ai.git
cd betaroot-ai
```

#### 2. إنشاء بيئة افتراضية

```bash
# على Linux/Mac
python3 -m venv venv
source venv/bin/activate

# على Windows
python -m venv venv
venv\Scripts\activate
```

#### 3. تثبيت المتطلبات

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # إذا كانت موجودة
```

#### 4. التحقق من التثبيت

```bash
pytest tests/
```

### سير العمل (Workflow)

#### الخطوة 1: إنشاء فرع جديد

```bash
# استخدم أسماء وصفية للفروع
git checkout -b feature/اسم-الميزة
# أو
git checkout -b fix/اسم-الإصلاح
# أو
git checkout -b docs/تحديث-التوثيق
```

#### الخطوة 2: إجراء التغييرات

عند كتابة الكود، تذكر:

**أ) معايير الكود:**
```python
# ✅ صحيح
def process_unary_state(state: UnaryState) -> UnaryState:
    """Process a unary state and return transformed result.
    
    Args:
        state: Input unary state
        
    Returns:
        UnaryState: Transformed state
    """
    # Implementation
    pass

# ❌ خاطئ
def process(s):
    # process state
    return s
```

**ب) التعليقات:**
```python
# العربية + الإنجليزية حيث يكون مفيداً
# تحويل المدخل إلى تمثيل موحد
# Convert input to unified representation
result = unary_logic.encode(data)
```

**ج) الاختبارات:**
```python
# اكتب اختبارات لكل دالة جديدة
def test_encode_integer():
    """Test encoding of integer values"""
    engine = create_engine()
    state = engine.encode(42)
    assert state.level == RepresentationLevel.FIRST_ORDER
```

#### الخطوة 3: تشغيل الاختبارات

```bash
# تشغيل جميع الاختبارات
pytest tests/ -v

# تشغيل اختبارات محددة
pytest tests/test_unary_logic.py -v

# مع تغطية (Coverage)
pytest tests/ --cov=betaroot/
```

#### الخطوة 4: التحقق من جودة الكود

```bash
# تنسيق الكود
black betaroot/

# فحص الأخطاء
flake8 betaroot/

# فحص النوع
mypy betaroot/

# ترتيب الاستيرادات
isort betaroot/
```

#### الخطوة 5: الالتزام بالتغييرات (Commit)

```bash
# أضف التغييرات
git add .

# التزم برسالة واضحة
git commit -m "Feature: إضافة محرك الاستدلال الجديد

- وصف تفصيلي للتغيير
- سبب التغيير
- أي مشاكل يحلها

Closes #123"
```

**معايير رسائل الالتزام:**
- ابدأ برنوع الالتزام: `Feature:`, `Fix:`, `Docs:`, `Refactor:`, `Test:`
- استخدم الأمر الأول شخص: "إضافة" بدلاً من "أضفت"
- اشرح **لماذا** وليس فقط **ماذا**
- اربط بـ Issues إذا أغلقت أحدها: `Closes #123`

#### الخطوة 6: دفع التغييرات

```bash
git push origin feature/اسم-الميزة
```

#### الخطوة 7: فتح طلب دمج (Pull Request)

1. اذهب إلى GitHub
2. انقر على "New Pull Request"
3. اختر فرعك ضد `main`
4. ملئ النموذج:

```markdown
## الوصف
وصف موجز للتغييرات

## نوع التغيير
- [ ] ميزة جديدة
- [ ] إصلاح خلل
- [ ] تحديث التوثيق
- [ ] إعادة هيكلة

## الاختبارات
- [ ] أضفت اختبارات جديدة
- [ ] جميع الاختبارات تمر
- [ ] غطيت الحالات الحدية

## التوثيق
- [ ] حدثت التوثيق
- [ ] أضفت تعليقات واضحة
- [ ] حدثت ملف CHANGELOG

## قائمة التحقق
- [ ] اتبعت معايير الكود
- [ ] لا توجد تعارضات الدمج
```

---

### 📋 قائمة التحقق قبل الإرسال

قبل فتح طلب دمج، تأكد:

- [ ] **الكود نظيف:** `black`, `flake8`, `mypy` يمران بنجاح
- [ ] **الاختبارات:** جميع الاختبارات تمر و`coverage` > 80%
- [ ] **التوثيق:** كل دالة موثقة بـ docstrings
- [ ] **التعليقات:** الكود معلق بوضوح
- [ ] **Git نظيف:** لا توجد commits غير متعلقة
- [ ] **الرسالة:** واضحة وموجزة

---

### 🐛 الإبلاغ عن الأخطاء

إذا وجدت خطأ:

1. **تحقق أنه لم يُبلغ عنه سابقاً:** ابحث في [Issues](https://github.com/betaroot/betaroot-ai/issues)

2. **أنشئ Issue جديد** بهذا الشكل:

```markdown
## الوصف
وصف واضح للخطأ

## خطوات التكرار
1. قم بـ...
2. ثم...
3. يحدث...

## السلوك المتوقع
ماذا يجب أن يحدث

## السلوك الفعلي
ماذا يحدث فعلاً

## البيئة
- Python: 3.11.x
- OS: Linux/Mac/Windows
- Traceback: [إن وجد]
```

---

### 💡 اقتراح ميزات جديدة

لاقتراح ميزة:

1. **تحقق من المناقشات:** هل تم طرح الفكرة سابقاً؟
2. **فتح Discussion:** في [Discussions](https://github.com/betaroot/betaroot-ai/discussions)
3. **اشرح الفائدة:** لماذا هذه الميزة مهمة؟
4. **أعطِ أمثلة:** كيف ستُستخدم؟

---

### 📚 تحسين التوثيق

المساهمات في التوثيق مرحب بها:

```bash
# يمكنك تحديث:
- README.md
- docs/*.md
- Docstrings في الكود
- تعليقات الكود
```

---

### 🎓 الأكواد والأمثلة

إذا أضفت مثالاً أو كود توضيحي:

```python
"""
مثال: استخدام محرك الاستدلال

يوضح هذا المثال كيفية استخدام محرك الاستدلال
لحل مسائل منطقية بسيطة.
"""

from betaroot import BetaRoot

br = BetaRoot()

# إضافة حقائق
br.knowledge_base.add_fact("fact1", "كل البشر فانون")
br.knowledge_base.add_fact("fact2", "أرسطو بشر")

# الاستدلال
result = br.process("هل أرسطو فان؟")

print(result['reasoning_path'])
# النتيجة: نعم
```

---

## English

---

## Contribution Guidelines

Thank you for your interest in contributing to BetaRoot! This document explains how to contribute effectively.

### Prerequisites

Before starting, ensure:
- ✅ You have a GitHub account
- ✅ Python 3.11+ installed
- ✅ Git installed
- ✅ You've read [PHILOSOPHY.md](docs/PHILOSOPHY.md)

### Getting Started

#### 1. Clone the Repository

```bash
git clone https://github.com/betaroot/betaroot-ai.git
cd betaroot-ai
```

#### 2. Create Virtual Environment

```bash
# On Linux/Mac
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # if available
```

#### 4. Verify Installation

```bash
pytest tests/
```

### Workflow

#### Step 1: Create New Branch

```bash
# Use descriptive branch names
git checkout -b feature/feature-name
# or
git checkout -b fix/bug-fix-name
# or
git checkout -b docs/documentation-update
```

#### Step 2: Make Changes

When writing code, remember:

**A) Code Standards:**
```python
# ✅ Correct
def process_unary_state(state: UnaryState) -> UnaryState:
    """Process a unary state and return transformed result.
    
    Args:
        state: Input unary state
        
    Returns:
        UnaryState: Transformed state
    """
    # Implementation
    pass

# ❌ Wrong
def process(s):
    # process state
    return s
```

**B) Comments:**
```python
# Both English and Arabic where helpful
# تحويل المدخل إلى تمثيل موحد
# Convert input to unified representation
result = unary_logic.encode(data)
```

**C) Tests:**
```python
# Write tests for every new function
def test_encode_integer():
    """Test encoding of integer values"""
    engine = create_engine()
    state = engine.encode(42)
    assert state.level == RepresentationLevel.FIRST_ORDER
```

#### Step 3: Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific tests
pytest tests/test_unary_logic.py -v

# With coverage
pytest tests/ --cov=betaroot/
```

#### Step 4: Check Code Quality

```bash
# Format code
black betaroot/

# Lint
flake8 betaroot/

# Type check
mypy betaroot/

# Sort imports
isort betaroot/
```

#### Step 5: Commit Changes

```bash
# Add changes
git add .

# Commit with clear message
git commit -m "Feature: Add new reasoning engine

- Detailed description of change
- Reason for change
- Problems it solves

Closes #123"
```

**Commit Message Standards:**
- Start with type: `Feature:`, `Fix:`, `Docs:`, `Refactor:`, `Test:`
- Use imperative mood: "Add" not "Added"
- Explain **why** not just **what**
- Link to Issues: `Closes #123`

#### Step 6: Push Changes

```bash
git push origin feature/feature-name
```

#### Step 7: Open Pull Request

1. Go to GitHub
2. Click "New Pull Request"
3. Select your branch against `main`
4. Fill the form:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update
- [ ] Refactoring

## Testing
- [ ] Added new tests
- [ ] All tests pass
- [ ] Edge cases covered

## Documentation
- [ ] Updated documentation
- [ ] Added clear comments
- [ ] Updated CHANGELOG

## Checklist
- [ ] Code follows standards
- [ ] No merge conflicts
```

---

### ✅ Pre-Submission Checklist

Before opening a PR, ensure:

- [ ] **Code is clean:** `black`, `flake8`, `mypy` pass
- [ ] **Tests pass:** All tests pass with >80% coverage
- [ ] **Documentation:** All functions have docstrings
- [ ] **Comments:** Code is clearly commented
- [ ] **Git is clean:** No unrelated commits
- [ ] **Message is clear:** Brief and descriptive

---

### 🐛 Reporting Bugs

If you find a bug:

1. **Check if reported:** Search [Issues](https://github.com/betaroot/betaroot-ai/issues)
2. **Create new Issue:**

```markdown
## Description
Clear description of the bug

## Steps to Reproduce
1. Do...
2. Then...
3. Happens...

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- Python: 3.11.x
- OS: Linux/Mac/Windows
- Traceback: [if available]
```

---

### 💡 Suggesting Features

To suggest a feature:

1. **Check discussions:** Has this been discussed?
2. **Open Discussion:** In [Discussions](https://github.com/betaroot/betaroot-ai/discussions)
3. **Explain benefit:** Why is this important?
4. **Give examples:** How would it be used?

---

### 📚 Improving Documentation

Documentation contributions are welcome:

```bash
# You can update:
- README.md
- docs/*.md
- Docstrings in code
- Code comments
```

---

### 🎓 Code Examples

If you add examples or demonstrations:

```python
"""
Example: Using the Reasoning Engine

Demonstrates how to use the reasoning engine
to solve simple logical problems.
"""

from betaroot import BetaRoot

br = BetaRoot()

# Add facts
br.knowledge_base.add_fact("fact1", "All humans are mortal")
br.knowledge_base.add_fact("fact2", "Aristotle is human")

# Reason
result = br.process("Is Aristotle mortal?")

print(result['reasoning_path'])
# Result: Yes
```

---

## 🎯 Areas Needing Help

Currently, we need help with:

1. **Core Implementation** - Unary logic, symbolic patterns
2. **Documentation** - Guides, examples, translations
3. **Testing** - Test coverage, edge cases
4. **Applications** - Real-world use cases
5. **Optimization** - Performance improvements

---

## 📞 Questions?

- **Discussions:** [GitHub Discussions](https://github.com/betaroot/betaroot-ai/discussions)
- **Issues:** [GitHub Issues](https://github.com/betaroot/betaroot-ai/issues)
- **Email:** contact@betaroot.dev

---

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please read our [Code of Conduct](CODE_OF_CONDUCT.md).

---

Thank you for contributing to BetaRoot! 🌳

