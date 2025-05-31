# backend/auth_service/services/auth.py

from auth_service.utils.security import verificar_senha, criar_token_acesso
from auth_service.models.user import buscar_usuario_por_email

def autenticar_usuario(email: str, senha: str) -> str:
    """
    Valida o usuário no MongoDB e retorna um token JWT se estiver correto.
    """
    usuario = buscar_usuario_por_email(email)
    if not usuario or not verificar_senha(senha, usuario["senha"]):
        raise Exception("Usuário ou senha inválidos")

    return criar_token_acesso({"sub": email})
