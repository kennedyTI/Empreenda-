# Rota POST /login – Autentica o usuário e retorna token JWT

from fastapi import APIRouter, Form, HTTPException
from auth_service.services.auth import autenticar_usuario
from auth_service.schemas.token import TokenResponse

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(username: str = Form(...), password: str = Form(...)):
    """
    Realiza login do usuário.
    Espera os dados via formulário (application/x-www-form-urlencoded).

    Retorna:
    - Token JWT de acesso, se login for bem-sucedido.
    """
    try:
        token = autenticar_usuario(username, password)
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
