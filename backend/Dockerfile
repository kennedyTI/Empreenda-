# Imagem base leve com Python 3.11
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências para dentro da imagem
COPY requirements.txt ./

# Instala as dependências listadas no requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos e pastas do projeto para dentro da imagem
COPY . .

# Comando padrão para iniciar a aplicação com Uvicorn
CMD ["uvicorn", "auth_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
