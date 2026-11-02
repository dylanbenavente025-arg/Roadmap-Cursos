# ---------- Etapa 1: builder (instala las dependencias; se descarta) ----------
FROM python:3.13-alpine AS builder

# uv con la versión registrada en el TRD
RUN pip install --no-cache-dir uv==0.13.5

ENV UV_PYTHON_DOWNLOADS=never \
    UV_LINK_MODE=copy

WORKDIR /app

# Solo las dependencias de producción, exactamente las de uv.lock.
# Después se borran archivos que no hacen falta para correr (fuentes C y cachés).
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev \
 && find /app/.venv \( -name "__pycache__" -o -name "*.c" -o -name "*.pyx" -o -name "*.pxd" \) -prune -exec rm -rf {} +

# ---------- Etapa 2: runtime (imagen final: solo lo necesario para correr) ----------
FROM python:3.13-alpine AS runtime

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Usuario sin privilegios: si alguien vulnera la app, no es root dentro del contenedor
RUN addgroup -S appuser && adduser -S -D -H -G appuser appuser

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY app ./app

USER appuser

EXPOSE 8000

# Docker consulta /health cada 10 s; tres fallos seguidos marcan el contenedor como unhealthy
HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]