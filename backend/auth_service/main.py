"""
Ponto de entrada da API de autenticação Empreenda+.
Registra rotas, valida conexão com MongoDB e aplica configurações específicas de ambiente.
"""

from fastapi import FastAPI
import os
import logging

# Configura logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rotas
from auth_service.routes.login import router as login_router
from auth_service.routes.protected import router as protected_router
from auth_service.routes.signup import router as signup_router

# Utilitários executados no início da aplicação
from auth_service.utils.verificar_mongodb import verificar_conexao_mongodb
from auth_service.utils.update_requirements import atualizar_requirements
from auth_service.utils.criar_usuario_mock import criar_usuario_mock

# Instancia a aplicação
app = FastAPI()

# Registra rotas
app.include_router(login_router)
app.include_router(protected_router)
app.include_router(signup_router)

# Rota pública para verificação (usada pelo frontend ou monitoring)
@app.get("/ping")
def ping():
    return {"ok": True}

@app.on_event("startup")
def startup_event():
    logger.info("🔄 Iniciando Auth Service...")

    # Garante que a conexão com MongoDB esteja disponível
    verificar_conexao_mongodb()

    if os.getenv("ENV") == "dev":
        criar_usuario_mock()
        atualizar_requirements()

# Apenas em dev: rota para teste de envio de e-mail
if os.getenv("ENV") == "dev":
    from auth_service.utils.email_service import enviar_email

    @app.get("/enviar-email-teste")
    def email_teste():
        sucesso = enviar_email(
            destinatario="kennedy.tads@gmail.com",
            assunto="🔐 Teste de E-mail - Empreenda+",
            corpo="Este é um teste de envio automático."
        )
        return {"status": "sucesso" if sucesso else "erro"}
