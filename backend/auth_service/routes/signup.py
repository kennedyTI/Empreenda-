# auth_service/routes/signup.py

from fastapi import APIRouter, HTTPException, Request
from auth_service.schemas.user import SignupRequest, SignupResponse  # Schemas para entrada e saída
from auth_service.services.user_service import criar_usuario         # Serviço para criação no MongoDB
from auth_service.utils.limiter import verificar_limite_ip           # Proteção contra spam por IP

router = APIRouter()  # Cria o roteador

@router.post("/signup", response_model=SignupResponse)
def signup(request: Request, dados: SignupRequest):
    """
    Rota responsável por cadastrar um novo usuário.

    Funcionalidades:
    - Limita requisições consecutivas por IP (proteção contra spam temporária).
    - Valida os dados via Pydantic (nome, email, senha).
    - Persiste o usuário no MongoDB.
    - Retorna mensagem de sucesso com o ID gerado.
    """

    # 🚫 Verifica se o IP ultrapassou o limite de requisições permitidas
    ip = request.client.host
    verificar_limite_ip(ip)

    try:
        # Cria o usuário no banco
        user_id = criar_usuario(dados)

        # Retorna confirmação com ID
        return SignupResponse(mensagem="Usuário criado com sucesso", id=str(user_id))

    except HTTPException as e:
        # Lança exceções previstas (ex: email duplicado)
        raise e

    except Exception as e:
        # Erros inesperados (ex: falha no Mongo)
        raise HTTPException(status_code=500, detail=f"Erro ao cadastrar usuário: {e}")
