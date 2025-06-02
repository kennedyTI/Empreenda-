# Schemas de entrada e saída relacionados ao usuário (signup)

from pydantic import BaseModel, EmailStr, Field

class SignupRequest(BaseModel):
    """
    Esquema de entrada para criação de novo usuário via /signup.
    """
    nome: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    senha: str = Field(..., min_length=6, max_length=100)


class SignupResponse(BaseModel):
    """
    Esquema de saída após criação de usuário.
    """
    mensagem: str
    id: str
