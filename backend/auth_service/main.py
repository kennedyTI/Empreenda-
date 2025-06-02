from fastapi import FastAPI
import os
import logging

# Configura logging para exibir mensagens de nível INFO no console
logging.basicConfig(level=logging.INFO)

# Importa os roteadores (rotas)
from auth_service.routes.login import router as login_router
from auth_service.routes.protected import router as protected_router
from auth_service.routes.signup import router as signup_router

# Importa funções utilitárias
from auth_service.utils.verificar_mongodb import verificar_conexao_mongodb
from auth_service.utils.update_requirements import atualizar_requirements
from auth_service.utils.criar_usuario_mock import criar_usuario_mock

# Cria a instância principal do FastAPI
app = FastAPI()

# Registra os roteadores no app
app.include_router(login_router)
app.include_router(protected_router)
app.include_router(signup_router)

# Rota simples para verificar se a API está online
@app.get("/ping")
def ping():
    return {"ok": True}

# Evento executado automaticamente quando o FastAPI iniciar
@app.on_event("startup")
def startup_event():
    # Valida se a conexão com o MongoDB está OK
    verificar_conexao_mongodb()

    # Executa ações extras se estivermos em ambiente de desenvolvimento
    if os.getenv("ENV", "dev") == "dev":
        criar_usuario_mock()
        atualizar_requirements()
