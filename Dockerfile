# ==========================================
# Stage 1: Build & Install Dependencies
# ==========================================
FROM python:3.11-slim AS builder
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build
# نسخ ملفات التعريف أولاً للاستفادة من Docker Layer Caching
COPY pyproject.toml README.md ./
COPY betaroot/ ./betaroot/

# تثبيت المكتبات الأساسية + أدوات التطوير
RUN pip install --upgrade pip && \
    pip install --no-cache-dir ".[dev]"

# ==========================================
# Stage 2: Runtime (Production)
# ==========================================
FROM python:3.11-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    BETA_ROOT_ENV=production

WORKDIR /app

# نسخ الحزم المترتبة من مرحلة البناء
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# نسخ الكود المصدري
COPY --from=builder /build/betaroot ./betaroot
COPY README.md .

# فحص صحة التثبيت
RUN python -c "import betaroot; print('✅ BetaRoot core modules loaded successfully.')"

# منفذ اختياري (في حال إضافة FastAPI لاحقاً)
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import betaroot; import sys; sys.exit(0)" || exit 1

CMD ["betaroot-cli", "--help"]

# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
