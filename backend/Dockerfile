# Imagen de desarrollo, simple y de una sola etapa (multi-stage queda para otra clase).
FROM python:3.13-slim

# uv con la versión registrada en el TRD
RUN pip install --no-cache-dir uv==0.13.5

# El entorno virtual vive fuera de /app y sus comandos quedan en el PATH
ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_PYTHON_DOWNLOADS=never \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Primero las dependencias (fijadas por uv.lock), después el código
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY app ./app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]