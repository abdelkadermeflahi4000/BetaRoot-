#!/bin/bash
# BetaRoot Auto Launcher
# مجرد تشغيل هذا السكريبت بعد الـ clone

set -e

echo "🚀 جاري تشغيل BetaRoot تلقائياً..."

# 1. التحقق من Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 غير موجود. يرجى تثبيته أولاً."
    exit 1
fi

# 2. إنشاء بيئة افتراضية
if [ ! -d "venv" ]; then
    echo "📦 إنشاء بيئة افتراضية..."
    python3 -m venv venv
fi

# 3. تفعيل البيئة وتثبيت المتطلبات
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .   # تثبيت BetaRoot كـ editable package

echo "✅ تم التثبيت بنجاح!"

# 4. تشغيل المحرك (غير هذا حسب الـ entry point الخاص بك)
echo "🔥 تشغيل محرك BetaRoot..."
python -m betaroot.core.betaroot   # أو betaroot run أو python examples_phase1.py

# أو إذا كان لديك CLI:
# betaroot demo
