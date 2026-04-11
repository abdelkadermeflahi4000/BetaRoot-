#!/usr/bin/env bash
# publish.sh - Safe & automated PyPI publishing for BetaRoot
# Usage: ./publish.sh [--test] [--dry-run]
set -euo pipefail

# ألوان للوضوح
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 بدء عملية نشر BetaRoot...${NC}"

# 1. التحقق من النظافة البرمجية
if [[ -n "$(git status --porcelain)" ]]; then
    echo -e "${RED}⚠️  يوجد تغييرات غير مرحّلة (uncommitted). يرجى commit كل شيء أولاً.${NC}"
    exit 1
fi

# 2. تحليل المعطيات
TEST_PYPI=false
DRY_RUN=false
for arg in "$@"; do
    case $arg in
        --test) TEST_PYPI=true ;;
        --dry-run) DRY_RUN=true ;;
    esac
done

# 3. تثبيت أدوات البناء إذا لزم الأمر
if ! command -v python3 -m build &> /dev/null; then
    echo -e "${YELLOW}📦 تثبيت أدوات البناء...${NC}"
    pip install --quiet build twine
fi

# 4. تشغيل الاختبارات
echo -e "${YELLOW}🧪 تشغيل اختبارات التكامل...${NC}"
if pytest tests/ -q; then
    echo -e "${GREEN}✅ جميع الاختبارات نجحت.${NC}"
else
    echo -e "${RED}❌ فشلت بعض الاختبارات. تم إيقاف النشر.${NC}"
    exit 1
fi

# 5. تنظيف مجلد التوزيع السابق
rm -rf dist/ build/ *.egg-info

# 6. بناء الحزمة
echo -e "${YELLOW}📦 بناء الحزمة (sdist + wheel)...${NC}"
python3 -m build
echo -e "${GREEN}✅ تم بناء الحزمة بنجاح.${NC}"

# 7. التحقق من جودة الحزمة
twine check dist/*

# 8. النشر
if [[ "$DRY_RUN" == true ]]; then
    echo -e "${YELLOW}🌪️ وضع Dry-Run: تم التحقق فقط دون رفع.${NC}"
else
    INDEX_URL="https://upload.pypi.org/legacy/"
    [[ "$TEST_PYPI" == true ]] && INDEX_URL="https://test.pypi.org/legacy/"

    echo -e "${YELLOW}📤 جاري الرفع إلى $INDEX_URL ...${NC}"
    # ملاحظة: يُفضل استخدام متغيرات البيئة TWINE_USERNAME و TWINE_PASSWORD
    python3 -m twine upload \
        --repository-url "$INDEX_URL" \
        --skip-existing \
        dist/*
    
    echo -e "${GREEN}✅ تم النشر بنجاح!${NC}"
    
    # وضع وسم Git تلقائي
    VERSION=$(python3 -c "import tomllib; print(tomllib.load(open('pyproject.toml', 'rb'))['project']['version'])")
    git tag -a "v$VERSION" -m "Release v$VERSION"
    git push origin "v$VERSION"
    echo -e "${GREEN}🏷️ تم إنشاء ودفع وسم Git: v$VERSION${NC}"
fi

echo -e "${GREEN}🎉 انتهت عملية النشر بنجاح. شكراً لتطويرك لـ BetaRoot!${NC}"
