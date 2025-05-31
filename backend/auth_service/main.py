from fastapi import FastAPI
import os
import logging

# Configuração básica de logging para exibir informações no console
logging.basicConfig(level=logging.INFO)

# Importa os roteadores de autenticação e de rotas protegidas
from auth_service.routes.login import router as login_router
from auth_service.routes.protected import router as protected_router

# Importa função para verificar a conexão com o MongoDB
from auth_service.utils.verificar_mongodb import verificar_conexao_mongodb

# Importa função utilitária para atualizar o requirements.txt
from auth_service.utils.update_requirements import atualizar_requirements

# Cria a instância principal do FastAPI
app = FastAPI()

# Registra as rotas no app
app.include_router(login_router)
app.include_router(protected_router)

# Rota simples para verificar se a API está online
@app.get("/ping")
def ping():
    return {"ok": True}

# Evento de inicialização da aplicação FastAPI
@app.on_event("startup")
def startup_event():
    verificar_conexao_mongodb()

# Atualiza automaticamente o requirements.txt se estiver em ambiente de desenvolvimento
if os.getenv("ENV", "dev") == "dev":
    atualizar_requirements()

# Cria usuário fake no banco (somente em desenvolvimento)
from auth_service.utils.criar_usuario_mock import criar_usuario_mock
criar_usuario_mock()