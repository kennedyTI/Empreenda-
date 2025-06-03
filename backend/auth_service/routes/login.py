"""
Rota de login para o serviço de autenticação Empreenda+.
Autentica o usuário com e-mail e senha, e retorna um token JWT.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_401_UNAUTHORIZED

from auth_service.schemas.token import TokenResponse
from auth_service.services.auth import autenticar_usuario
from auth_service.utils.security import criar_token_acesso
from auth_service.utils.i18n import traduzir  # Suporte multilíngue

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    lang: str = Query("pt", description="Idioma da resposta: pt ou en")
):
    """
    Endpoint de login (POST /login)
    
    Parâmetros:
    - form_data: formulário OAuth2 com 'username' e 'password'
    - lang: idioma para mensagens de erro ('pt' ou 'en')

    Retorno:
    - 200 OK: { access_token, token_type }
    - 401 Unauthorized: token inválido
    """
    # Tenta autenticar usuário com os dados fornecidos
    usuario = autenticar_usuario(form_data.username, form_data.password)

    # Se não encontrar usuário ou senha estiver incorreta
    if not usuario:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=traduzir("token_invalido", lang)
        )

    # Gera e retorna token JWT com e-mail como "sub"
    access_token = criar_token_acesso({"sub": usuario["email"]})
    return TokenResponse(access_token=access_token, token_type="bearer")
