# auth_service/routes/login.py

from fastapi import APIRouter, Depends, HTTPException, Form, Query
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_401_UNAUTHORIZED
from auth_service.schemas.token import TokenResponse
from auth_service.services.auth import autenticar_usuario
from auth_service.utils.security import criar_token_acesso
from auth_service.utils.i18n import traduzir  # ✅ Suporte multilíngue

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    lang: str = Query("pt", description="Idioma da resposta: pt ou en")
):
    """
    Rota de login. Autentica usuário e retorna token JWT.

    Parâmetros:
    - form_data: dados do formulário (username e password)
    - lang: idioma da resposta (pt ou en)

    Retorno:
    - access_token e tipo se credenciais forem válidas
    - HTTP 401 se falhar na autenticação
    """

    usuario = autenticar_usuario(form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=traduzir("token_invalido", lang)
        )

    # Gera token JWT com o e-mail no campo "sub"
    access_token = criar_token_acesso({"sub": usuario["email"]})
    return TokenResponse(access_token=access_token, token_type="bearer")
