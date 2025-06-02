# Schema de resposta para a rota /login

from pydantic import BaseModel

class TokenResponse(BaseModel):
    """
    Modelo de resposta ao login contendo o token JWT.
    """
    access_token: str
    token_type: str
