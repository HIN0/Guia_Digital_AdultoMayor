# Imagen de contenedor del backend FastAPI.
# La aplicación escucha en el puerto 7860 dentro del contenedor;
# el mapeo al puerto del host se define en docker-compose.yml.
FROM python:3.12-slim

# Dependencias de sistema (compiladores por si alguna lib las necesita)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Se ejecuta como usuario no-root (UID 1000) por buenas prácticas de seguridad
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    HF_HOME=/home/user/.cache/huggingface \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 1) Instalar PyTorch en su variante CPU ANTES que el resto.
#    sentence-transformers depende de torch. Si torch se resuelve desde PyPI,
#    pip baja la build con CUDA: ~2,5 GB de librerías NVIDIA (cuBLAS, cuDNN,
#    NCCL, Triton...) que no sirven de nada en un servidor sin tarjeta gráfica.
#    Eso dejaba la imagen final en 10,2 GB. Instalándolo primero desde el
#    índice CPU de PyTorch, el requisito queda satisfecho y pip no vuelve a
#    bajarlo al procesar requirements.txt.
#
#    El sufijo "+cpu" solo existe en el índice de PyTorch, así que fuerza a que
#    la rueda venga de ahí y no de PyPI. Para actualizar torch en el futuro,
#    cambiar la versión aquí y verificar que exista en:
#    https://download.pytorch.org/whl/cpu/torch/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
        --extra-index-url https://download.pytorch.org/whl/cpu \
        torch==2.13.0+cpu

# 2) Instalar el resto de dependencias de Python
COPY --chown=user:user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) Pre-descargar el modelo de embeddings EN EL BUILD.
#    Así el arranque del contenedor es rápido y no re-descarga ~470MB cada vez.
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')"

# 4) Copiar el resto del código del backend
COPY --chown=user:user . .

EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
