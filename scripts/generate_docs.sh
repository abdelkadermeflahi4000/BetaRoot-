#!/usr/bin/env bash
# scripts/generate_docs.sh
# Usage: bash scripts/generate_docs.sh [--serve|--build|--clean]
set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}📚 بدء إنشاء توثيق BetaRoot...${NC}"

# 1. تثبيت التبعيات المطلوبة
echo -e "${YELLOW}📦 فحص وتثبيت مكتبات التوثيق...${NC}"
pip install -q --upgrade \
  "mkdocs>=1.5" \
  "mkdocs-material>=9.0" \
  "mkdocstrings[python]>=0.24" \
  "pymdown-extensions>=10.0"

# 2. إنشاء هيكل مجلد docs/ إذا لم يوجد
DOCS_DIR="docs"
API_DIR="$DOCS_DIR/api"
mkdir -p "$DOCS_DIR" "$API_DIR"

# 3. توليد صفحات API تلقائياً من شجرة betaroot/
echo -e "${YELLOW}🔍 مسح الوحدات البرمجية وتوليد مراجع API...${NC}"
python3 - << 'PYEOF'
import os, pathlib

DOCS_API = pathlib.Path("docs/api")
DOCS_API.mkdir(parents=True, exist_ok=True)

# ملف الفهرس الرئيسي
with open(DOCS_API / "index.md", "w", encoding="utf-8") as f:
    f.write("# 📡 API Reference\n\n")
    f.write("توليد تلقائي للواجهات البرمجية من شيفرة BetaRoot.\n\n")

# مسح كل ملفات .py في betaroot/ (باستثناء __init__.py و tests/)
for py_file in pathlib.Path("betaroot").rglob("*.py"):
    if py_file.name == "__init__.py" or "test" in str(py_file):
        continue

    # تحويل المسار إلى اسم module صحيح
    module_path = str(py_file.with_suffix("")).replace(os.sep, ".")
    md_name = py_file.with_suffix(".md").name
    md_file = DOCS_API / md_name

    with open(md_file, "w", encoding="utf-8") as f:
        f.write(f"---\ntitle: {module_path}\n---\n\n")
        f.write(f"# `{module_path}`\n\n")
        f.write(f"::: {module_path}\n")
    # تحديث الفهرس
    with open(DOCS_API / "index.md", "a", encoding="utf-8") as idx:
        idx.write(f"- [{module_path}]({md_name})\n")

print("✅ تم توليد مراجع API بنجاح.")
PYEOF

# 4. إنشاء صفحات أساسية إذا كانت مفقودة
for dir_name in "getting-started" "core" "memory" "goals" "examples"; do
  mkdir -p "$DOCS_DIR/$dir_name"
  if [ ! -f "$DOCS_DIR/$dir_name/overview.md" ]; then
    echo "# $dir_name\n\nمحتوى قيد الإنشاء..." > "$DOCS_DIR/$dir_name/overview.md"
  fi
done

# 5. تنفيذ الأمر المطلوب
case "${1:-}" in
  --serve)
    echo -e "${GREEN}🚀 تشغيل الخادم المحلي على http://127.0.0.1:8000${NC}"
    mkdocs serve --dev-addr 127.0.0.1:8000
    ;;
  --clean)
    echo -e "${YELLOW}🧹 تنظيف الملفات المولدة والمجلد site/..."
    rm -rf site/ docs/api/
    echo -e "${GREEN}✅ تم التنظيف."
    ;;
  *)
    echo -e "${GREEN}🏗️ بناء الموقع الثابت..."
    mkdocs build --clean --strict
    echo -e "${GREEN}✅ تم البناء بنجاح في مجلد site/"
    echo -e "${YELLOW}💡 للمعاينة المحلية: bash scripts/generate_docs.sh --serve"
    echo -e "${YELLOW}💡 للنشر على GitHub Pages: mkdocs gh-deploy"
    ;;
esac
