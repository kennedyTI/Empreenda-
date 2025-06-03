"""
Schema de resposta para a rota /login.
Retorna o token JWT e o tipo do token (geralmente "bearer").
"""

from pydantic import BaseModel

class TokenResponse(BaseModel):
    """
    Modelo de resposta ao login contendo o token JWT.

    Exemplo de resposta:
    {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
        "token_type": "bearer"
    }
    """
    access_token: str
    token_type: str
