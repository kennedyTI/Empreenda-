"""
Serviço de autenticação de usuário via e-mail e senha.
Responsável por validar as credenciais e gerar o token JWT.
"""

from auth_service.utils.security import verificar_senha, criar_token_acesso
from auth_service.services.user_service import buscar_usuario_por_email

def autenticar_usuario(email: str, senha: str) -> str:
    """
    Autentica um usuário buscando pelo e-mail no MongoDB.
    Valida a senha com bcrypt e retorna um token JWT se for válida.

    Parâmetros:
    - email: e-mail do usuário
    - senha: senha em texto plano

    Retorna:
    - Token JWT válido para uso nas rotas protegidas

    Lança:
    - Exception (capturada por quem consome esta função)
    """
    usuario = buscar_usuario_por_email(email)

    # Valida existência do usuário e a senha informada
    if not usuario or not verificar_senha(senha, usuario["senha"]):
        raise Exception("Usuário ou senha inválidos")

    # Gera o JWT com o campo 'sub' contendo o e-mail
    return criar_token_acesso({"sub": email})
