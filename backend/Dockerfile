# Dockerfile - Backend (FastAPI)

# Etapa 1: construtor
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt ./
RUN pip install --user --no-cache-dir -r requirements.txt

# Etapa 2: imagem final
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
ENV PATH="/root/.local/bin:$PATH"
COPY . .

CMD ["uvicorn", "auth_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
