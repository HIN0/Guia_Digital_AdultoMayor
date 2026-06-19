# Backend FastAPI para Hugging Face Spaces (Docker SDK)
# HF Spaces espera que la app escuche en el puerto 7860.
FROM python:3.12-slim

# Dependencias de sistema (compiladores por si alguna lib las necesita)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# HF Spaces recomienda correr como usuario no-root con UID 1000
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    HF_HOME=/home/user/.cache/huggingface \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 1) Instalar dependencias de Python
COPY --chown=user:user requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 2) Pre-descargar el modelo de embeddings EN EL BUILD.
#    Así el arranque del contenedor es rápido y no re-descarga ~470MB cada vez.
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')"

# 3) Copiar el resto del código del backend
COPY --chown=user:user . .

EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
