# backend/auth_service/routes/login.py
# Roteador de autenticação com rota POST /login

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from auth_service.schemas import TokenResponse
from auth_service.services.auth import autenticar_usuario

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Rota de login usando formulário OAuth2 (username=Email, password=Senha)
    Retorna JWT se autenticação for válida
    """
    token = autenticar_usuario(form_data.username, form_data.password)
    return {"access_token": token, "token_type": "bearer"}
