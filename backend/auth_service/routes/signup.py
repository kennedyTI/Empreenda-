# auth_service/routes/signup.py

from fastapi import APIRouter, HTTPException, Request, Header
from auth_service.schemas.user import SignupRequest, SignupResponse
from auth_service.services.user_service import criar_usuario
from auth_service.utils.limiter import verificar_limite_ip
from auth_service.utils.i18n import traduzir  # 🧠 Função de tradução

router = APIRouter()

@router.post("/signup", response_model=SignupResponse)
def signup(
    request: Request,
    dados: SignupRequest,
    accept_language: str = Header(default="pt")  # 📌 Lê idioma do header
):
    """
    Rota responsável por cadastrar um novo usuário.

    Funcionalidades:
    - Limita requisições consecutivas por IP (proteção contra spam temporária).
    - Valida os dados via Pydantic (nome, email, senha).
    - Persiste o usuário no MongoDB.
    - Retorna mensagem de sucesso com o ID gerado.
    - Tradução automática baseada no header Accept-Language.
    """
    # 🚫 Verifica se o IP ultrapassou o limite de requisições permitidas
    ip = request.client.host
    verificar_limite_ip(ip)

    try:
        # Cria o usuário no banco
        user_id = criar_usuario(dados)

        # ✅ Mensagem traduzida de sucesso
        msg = traduzir("signup.success", accept_language)

        return SignupResponse(mensagem=msg, id=str(user_id))

    except HTTPException as e:
        # Substitui a mensagem se for conhecida
        e.detail = traduzir(e.detail, accept_language)
        raise e

    except Exception as e:
        # Mensagem genérica em caso de erro desconhecido
        raise HTTPException(
            status_code=500,
            detail=traduzir("signup.error", accept_language)
        )
