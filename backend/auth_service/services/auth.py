# Serviço de autenticação de usuário via e-mail e senha

from auth_service.utils.security import verificar_senha, criar_token_acesso
from auth_service.services.user_service import buscar_usuario_por_email

def autenticar_usuario(email: str, senha: str) -> str:
    """
    Autentica um usuário buscando pelo e-mail no MongoDB.
    Valida a senha e retorna um token JWT se for válida.

    Parâmetros:
    - email: e-mail do usuário
    - senha: senha em texto plano

    Retorna:
    - JWT válido para uso nas rotas protegidas

    Lança:
    - Exception se as credenciais forem inválidas
    """
    usuario = buscar_usuario_por_email(email)
    if not usuario or not verificar_senha(senha, usuario["senha"]):
        raise Exception("Usuário ou senha inválidos")

    return criar_token_acesso({"sub": email})
