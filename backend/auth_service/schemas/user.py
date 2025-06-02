# auth_service/schemas/user.py

from pydantic import BaseModel, Field, field_validator
from pydantic import model_validator  # ✅ Para validações de modelo em Pydantic v2
from email_validator import validate_email, EmailNotValidError


class SignupRequest(BaseModel):
    """
    Esquema de entrada para criação de um novo usuário via /signup.
    Inclui validações:
    - Nome mínimo de 2 caracteres
    - Senha mínima de 8 caracteres
    - E-mail com validação real
    - Confirmação de senha
    """

    nome: str = Field(..., min_length=2, example="João Silva")
    email: str = Field(..., example="joao@exemplo.com")
    senha: str = Field(..., min_length=8, example="senhaSegura123")
    confirmar_senha: str = Field(..., min_length=8, example="senhaSegura123")

    @field_validator("email")
    def validar_email(cls, v):
        """
        Valida o e-mail com o pacote email-validator.
        Garante que o formato seja válido.
        """
        try:
            validate_email(v)
            return v
        except EmailNotValidError:
            raise ValueError("E-mail inválido")

    @model_validator(mode="after")
    def verificar_senhas_iguais(self) -> 'SignupRequest':
        """
        Verifica se os campos 'senha' e 'confirmar_senha' são iguais.
        Executado após a validação individual de campos.
        """
        if self.senha != self.confirmar_senha:
            raise ValueError("As senhas não conferem.")
        return self


class SignupResponse(BaseModel):
    """
    Esquema de saída para a resposta da rota /signup.
    Retorna uma mensagem de sucesso e o ID do usuário criado.
    """
    mensagem: str
    id: str
