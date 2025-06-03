"""
Rota de cadastro de novos usuários para o sistema Empreenda+.
Valida dados, aplica proteção contra spam e armazena o usuário no MongoDB.
"""

from fastapi import APIRouter, HTTPException, Request, Header
from auth_service.schemas.user import SignupRequest, SignupResponse
from auth_service.services.user_service import criar_usuario
from auth_service.utils.limiter import verificar_limite_ip
from auth_service.utils.i18n import traduzir  # Suporte a múltiplos idiomas

router = APIRouter()

@router.post("/signup", response_model=SignupResponse)
def signup(
    request: Request,
    dados: SignupRequest,
    accept_language: str = Header(default="pt")  # Detecta idioma via header
):
    """
    POST /signup

    - Valida dados de cadastro (nome, email, senha, confirmar_senha).
    - Aplica limiter de IP (prevenção contra spam).
    - Cria usuário no MongoDB.
    - Responde com ID e mensagem traduzida.
    """

    # Extrai IP do cliente (para limiter temporário)
    ip = request.client.host
    verificar_limite_ip(ip)

    try:
        # Cria o usuário no banco
        user_id = criar_usuario(dados)

        # Retorna mensagem traduzida e o ID gerado
        msg = traduzir("signup.success", accept_language)
        return SignupResponse(mensagem=msg, id=str(user_id))

    except HTTPException as e:
        # Aplica tradução à exceção tratada
        e.detail = traduzir(e.detail, accept_language)
        raise e

    except Exception:
        # Retorna erro genérico (traduzido)
        raise HTTPException(
            status_code=500,
            detail=traduzir("signup.error", accept_language)
        )
